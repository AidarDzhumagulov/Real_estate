<template>
  <div class="image-gallery">
    <div v-if="processedImages.length === 0" class="no-images">
      <div class="no-images-placeholder">
        📷 Нет изображений
      </div>
    </div>
    
    <div v-else class="images-container">
      <!-- Основное изображение -->
      <div class="main-image" v-if="processedImages.length > 0">
        <img 
          :src="getCurrentImageUrl()"
          :alt="currentImage.filename || 'Изображение объявления'"
          @error="handleImageError"
          @load="handleImageLoad"
          class="main-img"
          :key="currentImage.id"
        />
        
        <!-- Навигация между изображениями -->
        <div v-if="processedImages.length > 1" class="navigation">
          <button 
            @click="previousImage" 
            class="nav-btn prev-btn"
            :disabled="currentIndex === 0"
          >
            ‹
          </button>
          <button 
            @click="nextImage" 
            class="nav-btn next-btn"
            :disabled="currentIndex === processedImages.length - 1"
          >
            ›
          </button>
        </div>
        
        <!-- Индикатор количества изображений -->
        <div v-if="processedImages.length > 1" class="image-counter">
          {{ currentIndex + 1 }} / {{ processedImages.length }}
        </div>
      </div>
      
      <!-- Миниатюры (если больше одного изображения) -->
      <div v-if="processedImages.length > 1" class="thumbnails">
        <div 
          v-for="(image, index) in processedImages" 
          :key="image.id || index"
          class="thumbnail"
          :class="{ active: index === currentIndex }"
          @click="setCurrentImage(index)"
        >
          <img 
            :src="getImageUrl(image)"
            :alt="image.filename || `Изображение ${index + 1}`"
            @error="handleThumbnailError"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ImageGallery',
  props: {
    images: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      currentIndex: 0,
      loadingImages: new Set(),
      errorImages: new Set(),
      blobUrls: new Map() // Кэш для blob URLs
    };
  },
  computed: {
    processedImages() {
      // Фильтруем и обрабатываем изображения
      return this.images.filter(image => {
        // Проверяем, что изображение имеет необходимые данные
        return image && (image.url || image.src || image.id);
      });
    },
    
    currentImage() {
      return this.processedImages[this.currentIndex] || {};
    }
  },
  watch: {
    images: {
      handler() {
        // Сброс индекса при изменении списка изображений
        this.currentIndex = 0;
        this.errorImages.clear();
        this.loadingImages.clear();
        // Очищаем старые blob URLs
        this.blobUrls.forEach(url => URL.revokeObjectURL(url));
        this.blobUrls.clear();
      },
      deep: true
    }
  },
  beforeUnmount() {
    // Освобождаем blob URLs при уничтожении компонента
    this.blobUrls.forEach(url => URL.revokeObjectURL(url));
  },
  methods: {
    getCurrentImageUrl() {
      return this.getImageUrl(this.currentImage);
    },
    
    getImageUrl(image) {
      if (!image) return '';
      
      // Проверяем кэш blob URLs
      if (this.blobUrls.has(image.id)) {
        return this.blobUrls.get(image.id);
      }
      
      // Если есть готовый URL
      if (image.url) {
        return this.addAuthToUrl(image.url);
      }
      
      // Если есть src
      if (image.src) {
        return this.addAuthToUrl(image.src);
      }
      
      // Если есть только ID, используем правильный API endpoint
      if (image.id) {
        const token = localStorage.getItem('authToken');
        // Используем правильный endpoint из вашего attachment.js
        return `http://localhost:8000/api/attachments/?id_=${image.id}&token=${encodeURIComponent(token)}`;
      }
      
      return '';
    },
    
    addAuthToUrl(url) {
      const token = localStorage.getItem('authToken');
      if (!token) return url;
      
      // Проверяем, есть ли уже параметры в URL
      const separator = url.includes('?') ? '&' : '?';
      return `${url}${separator}token=${encodeURIComponent(token)}`;
    },
    
    nextImage() {
      if (this.currentIndex < this.processedImages.length - 1) {
        this.currentIndex++;
      }
    },
    
    previousImage() {
      if (this.currentIndex > 0) {
        this.currentIndex--;
      }
    },
    
    setCurrentImage(index) {
      this.currentIndex = index;
    },
    
    async handleImageError(event) {
      const image = this.currentImage;
      console.error('Ошибка загрузки изображения:', event.target.src);
      this.errorImages.add(this.currentIndex);
      
      // Пробуем альтернативные способы загрузки
      await this.tryAlternativeImageLoad(event.target, image);
    },
    
    handleThumbnailError(event) {
      console.error('Ошибка загрузки миниатюры:', event.target.src);
      // Устанавливаем placeholder для миниатюры
      event.target.style.display = 'none';
    },
    
    // handleImageLoad(event) {
    //   console.log('Изображение успешно загружено:', event.target.src);
    // },
    
    async tryAlternativeImageLoad(imgElement, image) {
      if (!image || !image.id) return;
      
      const token = localStorage.getItem('authToken');
      if (!token) return;
      
      // Список альтернативных URL для попыток
      const alternativeUrls = [
        `http://localhost:8000/api/attachments/?id_=${image.id}`,
        `http://localhost:8000/api/attachments/${image.id}`,
        `http://localhost:8000/api/attachments/download/${image.id}`,
        `http://localhost:8000/api/files/${image.id}`,
      ];
      
      for (const url of alternativeUrls) {
        try {
          const response = await fetch(url, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Accept': 'image/*'
            }
          });
          
          if (response.ok) {
            const blob = await response.blob();
            const blobUrl = URL.createObjectURL(blob);
            
            // Кэшируем blob URL
            this.blobUrls.set(image.id, blobUrl);
            
            // Обновляем изображение
            imgElement.src = blobUrl;
            console.log('Изображение успешно загружено через альтернативный URL:', url);
            return;
          }
        } catch (error) {
          console.error(`Ошибка загрузки через ${url}:`, error);
          continue;
        }
      }
      
      // Если все попытки неудачны, показываем placeholder
      this.showImagePlaceholder(imgElement);
    },
    
    showImagePlaceholder(imgElement) {
      // Создаем простой placeholder
      const canvas = document.createElement('canvas');
      canvas.width = 300;
      canvas.height = 200;
      const ctx = canvas.getContext('2d');
      
      // Рисуем серый фон
      ctx.fillStyle = '#f0f0f0';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Рисуем текст
      ctx.fillStyle = '#999';
      ctx.font = '16px Arial';
      ctx.textAlign = 'center';
      ctx.fillText('Изображение недоступно', canvas.width / 2, canvas.height / 2);
      
      // Конвертируем в data URL и устанавливаем как src
      imgElement.src = canvas.toDataURL();
    },
    
    // Метод для предварительной загрузки изображений
    async preloadImages() {
      const token = localStorage.getItem('authToken');
      if (!token) return;
      
      for (const image of this.processedImages) {
        if (!image.id || this.blobUrls.has(image.id)) continue;
        
        try {
          const response = await fetch(`http://localhost:8000/api/attachments/?id_=${image.id}`, {
            headers: {
              'Authorization': `Bearer ${token}`,
              'Accept': 'image/*'
            }
          });
          
          if (response.ok) {
            const blob = await response.blob();
            const blobUrl = URL.createObjectURL(blob);
            this.blobUrls.set(image.id, blobUrl);
          }
        } catch (error) {
          console.error('Ошибка предварительной загрузки:', error);
        }
      }
    }
  },
  
  async mounted() {
    // Предварительно загружаем изображения при монтировании компонента
    if (this.processedImages.length > 0) {
      await this.preloadImages();
    }
  }
};
</script>

<style scoped>
.image-gallery {
  width: 100%;
  height: 100%;
}

.no-images {
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
}

.no-images-placeholder {
  color: #6c757d;
  font-size: 1.1rem;
  text-align: center;
}

.images-container {
  width: 100%;
  height: 100%;
}

.main-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.main-img:hover {
  transform: scale(1.05);
}

.navigation {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  pointer-events: none;
}

.nav-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  pointer-events: auto;
}

.nav-btn:hover:not(:disabled) {
  background: rgba(0, 0, 0, 0.7);
  transform: scale(1.1);
}

.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.image-counter {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.thumbnails {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  overflow-x: auto;
  padding: 5px 0;
}

.thumbnail {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.thumbnail.active {
  border-color: #3498db;
}

.thumbnail:hover {
  border-color: #3498db;
  opacity: 0.8;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Скрытие полосы прокрутки для webkit браузеров */
.thumbnails::-webkit-scrollbar {
  height: 4px;
}

.thumbnails::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 2px;
}

.thumbnails::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 2px;
}

.thumbnails::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

@media (max-width: 768px) {
  .main-image {
    height: 180px;
  }
  
  .nav-btn {
    width: 35px;
    height: 35px;
    font-size: 18px;
  }
  
  .thumbnail {
    width: 50px;
    height: 50px;
  }
}
</style>