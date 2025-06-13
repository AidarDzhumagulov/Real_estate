<template>
  <div class="real-estate-page">
    <div class="content-wrapper">
      <main>
        <div class="listings-container">
          <div class="listings-content">
            <h1>Недвижимость</h1>
            
            <div class="filters">
              <select v-model="selectedType" class="filter-select">
                <option value="">Все типы</option>
                <option value="apartment">Квартиры</option>
                <option value="house">Дома</option>
                <option value="commercial">Коммерческая недвижимость</option>
                <option value="land">Земельные участки</option>
              </select>
              
              <div class="price-filter">
                <input 
                  v-model.number="priceFrom" 
                  type="number" 
                  placeholder="Цена от" 
                  class="price-input"
                />
                <input 
                  v-model.number="priceTo" 
                  type="number" 
                  placeholder="Цена до" 
                  class="price-input"
                />
              </div>
            </div>

            <div v-if="isLoadingValue" class="loading-message">
              Загрузка объявлений...
            </div>

            <div v-else-if="filteredListings.length === 0" class="no-listings">
              Объявления не найдены
            </div>

            <div v-else class="listings-grid">
              <div v-for="item in filteredListings" 
                   :key="`listing-${item.id}`" 
                   class="listing-card">
                <div class="listing-images">
                  <ImageGallery :images="item.images || []" />
                </div>
                <div class="listing-content">
                  <h3>{{ item.title }}</h3>
                  <p class="property-type">{{ getPropertyTypeLabel(item.propertyType) }}</p>
                  <p class="price" v-if="item.price">{{ formatPrice(item.price) }} сом</p>
                  <p class="area" v-if="item.area">{{ item.area }} м²</p>
                  <p class="address" v-if="item.address">{{ item.address }}</p>
                  <p class="description">{{ item.description }}</p>
                  <div class="card-actions">
                    <button class="details-button" @click="showListingDetails(item)">
                      Подробнее
                    </button>
                    <button class="edit-button" @click="$emit('open-edit', item)">
                      Редактировать
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>

    <ListingDetailsModal 
      v-if="selectedListing"
      :listing="selectedListing"
      @close="selectedListing = null"
    />
  </div>
</template>

<script>
import ImageGallery from '../components/ImageGallery.vue';
import ListingDetailsModal from '../components/ListingDetailsModal.vue';

export default {
  name: 'RealEstate',
  components: {
    ImageGallery,
    ListingDetailsModal
  },
  inject: {
    getListings: { default: () => [] },
    isLoading: { default: () => false }
  },
  data() {
    return {
      selectedType: '',
      priceFrom: null,
      priceTo: null,
      selectedListing: null
    };
  },
  computed: {
    currentListings() {
      // Вызываем функцию для получения актуальных данных
      const listings = typeof this.getListings === 'function' ? this.getListings() : [];
      return Array.isArray(listings) ? listings : [];
    },
    isLoadingValue() {
      return typeof this.isLoading === 'function' ? this.isLoading() : false;
    },
    filteredListings() {
      return this.currentListings.filter(item => {
        if (!item) return false;
        
        // Фильтр по типу
        if (this.selectedType && item.propertyType !== this.selectedType) {
          return false;
        }
        
        // Фильтр по цене от
        if (this.priceFrom && (!item.price || item.price < this.priceFrom)) {
          return false;
        }
        
        // Фильтр по цене до
        if (this.priceTo && (!item.price || item.price > this.priceTo)) {
          return false;
        }
        
        return true;
      });
    }
  },
  methods: {
    formatPrice(price) {
      if (!price) return '0';
      return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    },
    getPropertyTypeLabel(type) {
      const types = {
        apartment: 'Квартира',
        house: 'Дом',
        commercial: 'Коммерческая недвижимость',
        land: 'Земельный участок'
      };
      return types[type] || type;
    },
    showListingDetails(listing) {
      this.selectedListing = listing;
    }
  }
};
</script>

<style scoped>
.real-estate-page {
  padding-top: 70px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  margin-bottom: 2rem;
  color: #2c3e50;
  font-size: 2.5rem;
  text-align: center;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
}

.price-filter {
  display: flex;
  gap: 1rem;
}

.price-input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 150px;
}

.loading-message, .no-listings {
  text-align: center;
  padding: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.listings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.listing-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
  background: white;
  display: flex;
  flex-direction: column;
}

.listing-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.listing-images {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.listing-content {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.listing-content h3 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.property-type {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.price {
  color: #27ae60;
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.75rem;
}

.area, .address {
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.description {
  color: #666;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.card-actions {
  margin-top: auto;
}

.details-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #329de3;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.details-button:hover {
  background-color: #0562f7;
}

.edit-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 0.5rem;
}

.edit-button:hover {
  background-color: #27ae60;
}

@media (max-width: 768px) {
  .filters {
    flex-direction: column;
  }
  
  .price-filter {
    width: 100%;
  }
  
  .price-input {
    flex: 1;
  }
}
</style>