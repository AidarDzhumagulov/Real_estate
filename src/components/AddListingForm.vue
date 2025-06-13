<template>
  <div class="add-form-overlay">
    <div class="add-form">
      <h3>Добавить объявление</h3>
      <form @submit.prevent="submit">
        <!-- Название -->
        <div class="form-group">
          <label>Название</label>
          <input v-model="formData.title" type="text" required />
        </div>

        <!-- Тип недвижимости -->
        <div class="form-group">
          <label>Тип недвижимости</label>
          <select v-model="formData.property_type" required>
            <option value="">Выберите тип</option>
            <option value="apartment">Квартира</option>
            <option value="house">Дом</option>
            <option value="commercial">Коммерческая</option>
            <option value="land">Земельный участок</option>
          </select>
        </div>

        <!-- Цена и площадь -->
        <div class="form-row">
          <div class="form-group">
            <label>Цена (сом)</label>
            <input v-model="formData.price" type="number" required />
          </div>
          <div class="form-group">
            <label>Площадь (м²)</label>
            <input v-model="formData.area" type="number" />
          </div>
        </div>

        <!-- Комнаты и этаж (для квартир и домов) -->
        <div class="form-row" v-if="formData.property_type === 'apartment' || formData.property_type === 'house'">
          <div class="form-group">
            <label>Количество комнат</label>
            <input v-model="formData.rooms" type="number" min="1" />
          </div>
          <div class="form-group" v-if="formData.property_type === 'apartment'">
            <label>Этаж</label>
            <input v-model="formData.floor" type="number" min="1" />
          </div>
        </div>

        <!-- Адрес -->
        <div class="form-group">
          <label>Адрес</label>
          <input v-model="formData.address" type="text" required />
        </div>

        <!-- Город -->
        <div class="form-group">
          <label>Город</label>
          <input v-model="formData.city" type="text" required />
        </div>

        <!-- Описание -->
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="formData.description" required rows="4"></textarea>
        </div>

        <!-- Изображения -->
        <div class="form-group">
          <label>Фотографии</label>
          <input type="file" @change="handleImageUpload" multiple accept="image/*" />
          <div v-if="imagePreviewUrls.length" class="image-previews">
            <div v-for="(url, index) in imagePreviewUrls" :key="index" class="preview-container">
              <img :src="url" alt="Preview" class="preview-image" />
              <button type="button" @click="removeImage(index)" class="remove-image">&times;</button>
            </div>
          </div>
        </div>

        <!-- Кнопки -->
        <div class="form-actions">
          <button type="submit" class="submit-btn" :disabled="isSubmitting">
            {{ isSubmitting ? 'Добавление...' : 'Добавить' }}
          </button>
          <button type="button" class="cancel-btn" @click="cancel">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { createListing } from '../api/listings.js';
import { loadAttachment, uploadImage } from '../api/attachments.js';

export default {
  name: 'AddListingForm',
  data() {
    return {
      isSubmitting: false,
      formData: {
        title: '',
        property_type: '',
        price: '',
        area: '',
        rooms: '',
        floor: '',
        address: '',
        city: '',
        description: '',
      },
      imageFiles: [],
      imagePreviewUrls: []
    };
  },
  methods: {
    handleImageUpload(event) {
      const files = Array.from(event.target.files);
      this.imageFiles = files;

      this.imagePreviewUrls = [];
      files.forEach(file => {
        const reader = new FileReader();
        reader.onload = e => this.imagePreviewUrls.push(e.target.result);
        reader.readAsDataURL(file);
      });
    },

    removeImage(index) {
      this.imageFiles.splice(index, 1);
      this.imagePreviewUrls.splice(index, 1);
    },

    async uploadImages(files) {
      if (!files || files.length === 0) {
        return [];
      }

      const uploaded = [];
      const token = localStorage.getItem('authToken');

      for (const file of files) {
        try {
          const id = await uploadImage(file, token);
          uploaded.push(id);
        } catch (error) {
          console.error("Произошла ошибка при загрузке изображения:", error);
          const message = error.response?.data?.detail || error.message;
          alert("Не удалось загрузить изображение: " + message);
          throw error;
        }
      }

      return uploaded;
    },

    async loadAttachments(ids, token) {
      if (!ids || ids.length === 0) {
        return [];
      }

      const attachments = [];

      for (const id of ids) {
        try {
          const attachment = await loadAttachment(id, token);
          attachments.push(attachment);
        } catch (error) {
          console.error(`Не удалось получить attachment ${id}:`, error);
        }
      }
      return attachments;
    },

    async submit() {
      console.log('Начинаем отправку формы...');
      
      if (!this.validateForm()) {
        console.log('Валидация формы не прошла');
        return;
      }
      
      this.isSubmitting = true;
      const token = localStorage.getItem('authToken');

      if (!token) {
        alert('Для добавления объявления необходимо войти в систему');
        this.isSubmitting = false;
        return;
      }

      try {
        console.log('Загружаем изображения...');
        // Загружаем изображения
        const attachment_ids = await this.uploadImages(this.imageFiles);

        // Создаем объявление
        const payload = {
          ...this.formData,
          price: parseInt(this.formData.price) || 0,
          area: this.formData.area ? parseInt(this.formData.area) : null,
          rooms: this.formData.rooms ? parseInt(this.formData.rooms) : null,
          floor: this.formData.floor ? parseInt(this.formData.floor) : null,
          attachment_ids
        };

        const listing = await createListing(payload, token);
        console.log('Объявление создано:', listing);

        // Загружаем attachment'ы для получения URL изображений
        const attachments = await this.loadAttachments(attachment_ids, token);
        console.log('Attachments загружены:', attachments);

        // Преобразуем данные в формат, который ожидает интерфейс
        const listingForUI = {
          id: listing.id,
          title: listing.title,
          description: listing.description,
          price: listing.price,
          area: listing.area,
          address: listing.address,
          city: listing.city,
          propertyType: listing.property_type, // Преобразуем snake_case в camelCase
          rooms: listing.rooms,
          floor: listing.floor,
          images: attachments.map(att => att.url || att),
          attachments: attachments,
          createdAt: listing.created_at,
          updatedAt: listing.updated_at,
          // Добавляем другие поля если они есть
          ...listing
        };

        console.log('Отправляем данные родителю:', listingForUI);
        
        // Отправляем данные родительскому компоненту
        this.$emit("add", listingForUI);
        
        // Небольшая задержка перед сбросом формы
        setTimeout(() => {
          this.resetForm();
        }, 100);
        
        console.log('Объявление успешно создано');
        
      } catch (error) {
        console.error("Ошибка при создании объявления:", error);
        const message = error.response?.data?.detail || error.message;
        alert("Не удалось создать объявление: " + message);
      } finally {
        this.isSubmitting = false;
      }
    },

    validateForm() {
      const required = ["title", "property_type", "price", "address", "city", "description"];
      const isValid = required.every(field => this.formData[field]?.toString().trim());
      
      if (!isValid) {
        alert("Пожалуйста, заполните все обязательные поля");
        return false;
      }
      
      if (this.formData.price <= 0) {
        alert("Цена должна быть больше нуля");
        return false;
      }
      
      return true;
    },

    resetForm() {
      this.formData = {
        title: '',
        property_type: '',
        price: '',
        area: '',
        rooms: '',
        floor: '',
        address: '',
        city: '',
        description: ''
      };
      this.imageFiles = [];
      this.imagePreviewUrls = [];
    },

    cancel() {
      console.log('Отменяем добавление');
      this.resetForm();
      this.$emit('cancel');
    }
  }
};
</script>

<style scoped>
.add-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem;
  z-index: 1000;
  overflow-y: auto;
}

.add-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  margin: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 1.5rem;
  color: #2c3e50;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #02f98a;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.submit-btn, .cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-btn {
  background-color: #34db8a;
  color: white;
  flex: 2;
}

.submit-btn:hover:not(:disabled) {
  background-color: #37b929;
}

.submit-btn:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #bdc3c7;
  color: #2c3e50;
  flex: 1;
}

.cancel-btn:hover {
  background-color: #95a5a6;
}

/* Стили для превью изображений */
.image-previews {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 10px;
}

.preview-container {
  position: relative;
  width: 80px;
  height: 80px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-image {
  position: absolute;
  top: 2px;
  right: 2px;
  background: rgba(0, 0, 0, 0.5);
  border: none;
  color: white;
  font-size: 18px;
  line-height: 1;
  padding: 0 6px;
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.3s ease;
}

.remove-image:hover {
  background: rgba(0, 0, 0, 0.8);
}
</style>