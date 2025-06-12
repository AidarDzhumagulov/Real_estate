<template>
  <div id="app">
    <Header 
      @open-login="showLogin = true" 
      @open-add="showAddForm = true"
      @open-register="showRegister = true"
      @login-success="handleLoginSuccess"
      ref="header"
    />
    <div class="content-wrapper">
      <router-view 
        :listings="listings"
        :key="listingsKey"
        @open-add="showAddForm = true"
        @open-edit="editingListing = $event"
        @refresh-listings="loadListings"
      />
    </div>
    <LoginModal 
      v-if="showLogin" 
      @close="showLogin = false"
      @login-success="handleLoginSuccess"
    />
    <RegisterModal v-if="showRegister" @close="showRegister = false" />
    <AddListingForm 
      v-if="showAddForm" 
      @add="handleAdd" 
      @cancel="showAddForm = false" 
    />
    <EditListingForm 
      v-if="editingListing" 
      :listing="editingListing"
      @save="handleSave"
      @cancel="editingListing = null"
      @delete="handleDelete"
    />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import LoginModal from './components/Header/LoginModal.vue';
import RegisterModal from './components/Header/RegisterModal.vue';
import AddListingForm from './components/AddListingForm.vue';
import EditListingForm from './components/EditListingForm.vue';
import { getListing, deleteListing, updateListing } from './api/listings.js';
import { loadAttachment } from './api/attachments.js';
import { nextTick } from 'vue';

export default {
  name: 'App',
  components: {
    Header,
    LoginModal,
    RegisterModal,
    AddListingForm,
    EditListingForm
  },
  data() {
    return {
      showLogin: false,
      showRegister: false,
      showAddForm: false,
      editingListing: null,
      isLoading: false,
      listingsKey: 0,
      // Кэш для изображений, чтобы не загружать их повторно
      imageCache: new Map(),
      listings: [
        // Статические данные как fallback
        { 
          id: 'static-1',
          title: 'Современная 2-комнатная квартира',
          description: 'Светлая квартира с новым ремонтом',
          price: 45000,
          area: 65,
          address: 'ул. Токтогула 125',
          propertyType: 'apartment',
          rooms: 2,
          floor: 4,
          images: [],
          attachments: []
        },
        { 
          id: 'static-2',
          title: 'Просторный дом с участком',
          description: 'Двухэтажный дом с большим двором',
          price: 85000,
          area: 180,
          address: 'мкр. Асанбай, ул. Садовая 45',
          propertyType: 'house',
          rooms: 5,
          floor: 2,
          images: [],
          attachments: []
        },
      ]
    };
  },
  async created() {
    await this.initializeApp();
    window.addEventListener('user-logged-in', this.onGlobalLogin);
  },
  methods: {
    async initializeApp() {
      const token = localStorage.getItem('authToken');
      if (token) {
        await this.loadListings();
      }
    },

    unmounted() {
      window.removeEventListener('user-logged-in', this.onGlobalLogin);
    },

    async onGlobalLogin() {
      this.showLogin = false;
      await this.loadListings();
    },

    // Функция для загрузки данных изображения
    async loadImageData(attachmentId, token) {
      // Проверяем кэш
      if (this.imageCache.has(attachmentId)) {
        return this.imageCache.get(attachmentId);
      }

      try {
        const imageData = await loadAttachment(attachmentId, token);
        // Сохраняем в кэш
        this.imageCache.set(attachmentId, imageData);
        return imageData;
      } catch (error) {
        console.error(`Ошибка загрузки изображения ${attachmentId}:`, error);
        return null;
      }
    },

    // Функция для загрузки всех изображений объявления
    async loadListingImages(listing, token) {
      if (!listing.attachments || listing.attachments.length === 0) {
        return [];
      }

      const imagePromises = listing.attachments.map(attachment => 
        this.loadImageData(attachment.id, token)
      );

      try {
        const images = await Promise.all(imagePromises);
        // Фильтруем null значения (неудачные загрузки)
        return images.filter(img => img !== null);
      } catch (error) {
        console.error('Ошибка при загрузке изображений:', error);
        return [];
      }
    },

    async loadListings() {
      const token = localStorage.getItem('authToken');
      if (!token) {
        console.log('Нет токена для загрузки объявлений');
        return;
      }

      this.isLoading = true;
      try {
        const data = await getListing(token);
        
        if (!Array.isArray(data)) {
          console.error('API returned non-array data:', data);
          return;
        }
        
        // Создаем новый массив вместо мутации существующего
        const newListings = data.map(listing => ({
          id: listing.id,
          title: listing.title || 'Без названия',
          description: listing.description || 'Описание отсутствует',
          price: listing.price || 0,
          area: listing.area || 0,
          address: listing.address || 'Адрес не указан',
          city: listing.city || 'Город не указан',
          propertyType: listing.property_type || 'unknown',
          rooms: listing.rooms || 0,
          floor: listing.floor || 0,
          images: [], // Пока пустой массив
          attachments: listing.attachments || [],
          createdAt: listing.created_at,
          updatedAt: listing.updated_at,
          ...listing
        }));

        // Заменяем массив целиком
        this.listings = Object.freeze([...newListings]);
        
        // Ждем следующий тик для завершения рендеринга
        await nextTick();
        
        this.listingsKey++;

        // Загружаем изображения в следующем тике
        nextTick(() => {
          this.loadAllListingsImages(newListings, token);
        });
        
      } catch (error) {
        console.error('Ошибка при загрузке объявлений:', error);
        
        const message = error.response?.data?.detail || error.message;
        alert('Не удалось загрузить объявления: ' + message);
        
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          this.$refs.header?.updateAuthState();
        }
      } finally {
        this.isLoading = false;
      }
    },

    // Асинхронная загрузка изображений для всех объявлений
    async loadAllListingsImages(listings, token) {
      // Создаем копию текущих объявлений для безопасного обновления
      const updatedListings = [...this.listings];
      
      for (let i = 0; i < listings.length; i++) {
        const listing = listings[i];
        
        if (listing.attachments && listing.attachments.length > 0) {
          try {
            const images = await this.loadListingImages(listing, token);
            
            // Находим индекс объявления в актуальном массиве
            const listingIndex = updatedListings.findIndex(l => l.id === listing.id);
            if (listingIndex !== -1) {
              // Создаем новый объект вместо мутации
              updatedListings[listingIndex] = {
                ...updatedListings[listingIndex],
                images: images
              };
            }
          } catch (error) {
            console.error(`Ошибка загрузки изображений для объявления ${listing.id}:`, error);
          }
        }
        
        // Батчевое обновление каждые 3 объявления или в конце
        if (i % 3 === 0 || i === listings.length - 1) {
          await nextTick();
          this.listings = Object.freeze([...updatedListings]);
          this.listingsKey++;
        }
      }
    },

    async handleLoginSuccess() {
      this.showLogin = false;
      await this.loadListings();
    },

    async handleAdd(formData) {
      console.log('Получаем новое объявление в App.vue:', formData);
      
      try {
        // Сначала закрываем форму
        this.showAddForm = false;
        
        // Создаем новый массив с добавленным объявлением
        const newListing = {
          ...formData,
          images: formData.images || [],
          attachments: formData.attachments || []
        };
        
        this.listings = Object.freeze([newListing, ...this.listings]);
        this.listingsKey++;
        
        console.log('Объявление добавлено в список, общее количество:', this.listings.length);
        
        // Переходим на страницу недвижимости если мы не на ней
        if (this.$route.path !== '/real-estate') {
          await this.$router.push('/real-estate');
        }

        // Обновляем данные с сервера через некоторое время
        setTimeout(async () => {
          console.log('Обновляем данные с сервера...');
          await this.loadListings();
        }, 1000);
        
      } catch (error) {
        console.error('Ошибка при добавлении объявления:', error);
        // В случае ошибки все равно закрываем форму
        this.showAddForm = false;
      }
    },

    async handleSave(updatedListing) {
      
      if (!updatedListing || !updatedListing.id) {
        console.error('Некорректные данные объявления для обновления:', updatedListing);
        return;
      }

      const confirmed = confirm('Вы уверены, что хотите обновить это объявление?');
      if (!confirmed) {
        return;
      }

      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('Нет токена для обновления объявления');
        return;
      }

      this.isLoading = true;

      // Формируем payload из переданных данных
      const payload = {
        title: updatedListing.title,
        description: updatedListing.description,
        price: parseFloat(updatedListing.price) || 0,
        property_type: updatedListing.propertyType
      };


      try {
        const result = await updateListing(updatedListing.id, payload, token);
        
        // Закрываем форму редактирования
        this.editingListing = null;
        
        // Перезагружаем список объявлений
        await this.loadListings();
        
      } catch (error) {
        console.error('Ошибка при обновлении объявления:', error);
        alert('Произошла ошибка при обновлении. Попробуйте позже.');
      } finally {
        this.isLoading = false;
      }
    },
    async handleDelete(listing) {
      if (!listing || !listing.id) {
        console.error('Некорректные данные объявления для удаления:', listing);
        return;
      }

      const confirmed = confirm('Вы уверены, что хотите удалить это объявление?');
      if (!confirmed) {
        return;
      }

      console.log('Удаляем объявление с ID:', listing.id);

      const token = localStorage.getItem('authToken');
      if (!token) {
        console.error('Нет токена для удаления объявления');
        return;
      }

      this.isLoading = true;

      try {
        await deleteListing(listing.id, token);

        // Вместо локального обновления — сразу перезагружаем список
        await this.loadListings();

        this.editingListing = null;

      } catch (error) {
        console.error('Ошибка при удалении объявления:', error);
        alert('Произошла ошибка при удалении. Попробуйте позже.');
      } finally {
        this.isLoading = false;
      }
    },

    async refreshListings() {
      await this.loadListings();
    },

    // Метод для принудительной перезагрузки изображений
    async reloadImages() {
      this.imageCache.clear();
      const token = localStorage.getItem('authToken');
      if (token && this.listings.length > 0) {
        await this.loadAllListingsImages(this.listings, token);
      }
    }
  },
  
  provide() {
    return {
      // Возвращаем функции вместо прямых ссылок на данные
      listings: () => this.listings || [],
      getListings: () => this.listings || [],
      refreshListings: this.refreshListings,
      reloadImages: this.reloadImages,
      isLoading: () => this.isLoading
    };
  }
};
</script>

<style>
/* ... остальные стили остаются без изменений ... */
:root {
  --header-height: 70px;
  --container-max-width: 1200px;
  --container-padding: 1rem;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #2c3e50;
  background-color: #f8f9fa;
  overflow-x: hidden;
}

#app {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
}

.content-wrapper {
  flex: 1;
  width: 100%;
  padding: 0;
  overflow-x: hidden;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  font-size: 1.2rem;
  color: #2c3e50;
}

.container {
  width: 100%;
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding-left: var(--container-padding);
  padding-right: var(--container-padding);
}

h1 { 
  font-size: clamp(1.5rem, 4vw, 2.5rem); 
  margin: 0;
}
h2 { 
  font-size: clamp(1.25rem, 3vw, 2rem);
  margin: 0;
}
h3 { 
  font-size: clamp(1.1rem, 2.5vw, 1.75rem);
  margin: 0;
}
h4 { 
  font-size: clamp(1rem, 2vw, 1.5rem);
  margin: 0;
}
p { 
  font-size: clamp(0.875rem, 1.5vw, 1rem);
  margin: 0;
}

.section {
  padding: clamp(1.5rem, 5vw, 3rem) 0;
  width: 100%;
}

.grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  width: 100%;
}

img {
  max-width: 100%;
  height: auto;
  display: block;
}

button {
  padding: clamp(0.4rem, 1vw, 0.8rem) clamp(0.8rem, 2vw, 1.5rem);
  font-size: clamp(0.875rem, 1.5vw, 1rem);
}

@media (max-width: 768px) {
  :root {
    --container-padding: 1rem;
    --header-height: 60px;
  }

  .container {
    padding-left: var(--container-padding);
    padding-right: var(--container-padding);
  }

  .section {
    padding: 1rem 0;
  }
}

@media (max-width: 480px) {
  :root {
    --container-padding: 0.75rem;
  }
  
  .main-content {
    margin-top: var(--header-height);
  }

  button:not(.mobile-menu-btn) {
    width: 100%;
  }

  .grid {
    gap: 0.75rem;
  }
}
</style>