<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      
      <div class="listing-details">
        <div class="image-gallery">
          <ImageGallery :images="listing.images || []" />
        </div>

        <div class="details-content">
          <h2>{{ listing.title }}</h2>
          
          <div class="price-section">
            <span class="price">{{ formatPrice(listing.price) }} сом</span>
            <span class="property-type">{{ getPropertyTypeLabel(listing.propertyType) }}</span>
          </div>

          <div class="info-grid">
            <div class="info-item">
              <span class="label">Адрес:</span>
              <span class="value">{{ listing.address }}</span>
            </div>
            <div class="info-item">
              <span class="label">Количество комнат:</span>
              <span class="value">{{ listing.rooms || 'Не указано' }}</span>
            </div>
            <div class="info-item">
              <span class="label">Этаж:</span>
              <span class="value">{{ listing.floor || 'Не указано' }}</span>
            </div>
          </div>

          <div class="description-section">
            <h3>Описание</h3>
            <p>{{ listing.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ImageGallery from './ImageGallery.vue';

export default {
  name: 'ListingDetailsModal',
  components: {
    ImageGallery
  },
  props: {
    listing: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatPrice(price) {
      return price ? price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") : 'Цена не указана';
    },
    getPropertyTypeLabel(type) {
      const types = {
        apartment: 'Квартира',
        house: 'Дом',
        commercial: 'Коммерческая недвижимость',
        land: 'Земельный участок'
      };
      return types[type] || type;
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  z-index: 1;
}

.listing-details {
  display: flex;
  flex-direction: column;
}

.image-gallery {
  width: 100%;
  max-height: 400px;
  overflow: hidden;
}

.details-content {
  padding: 2rem;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.8rem;
}

.price-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #27ae60;
}

.property-type {
  background: #f0f2f5;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  color: #2c3e50;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item .label {
  color: #666;
  font-size: 0.9rem;
}

.info-item .value {
  color: #2c3e50;
  font-weight: 500;
}

.description-section {
  margin-bottom: 2rem;
}

h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
  }

  .details-content {
    padding: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .info-row {
    flex-direction: column;
    gap: 0.25rem;
  }

  .info-row .label {
    width: auto;
  }
}
</style> 