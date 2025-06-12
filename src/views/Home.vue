<template>
  <div class="home">
    <div class="content-wrapper">
      <HeroBanner />
      <main>
        <div id="listings" class="listings-container">
          <div class="listings-content">
            <!-- <h2>Срочная продажа</h2> -->
            <div v-if="isLoadingData" class="loading-message">
              Загрузка объявлений...
            </div>
            <div v-else-if="recentListings.length === 0" class="no-listings">
              Объявления не найдены
            </div>
            <div v-else class="listings-grid">
              <div v-for="(item, index) in recentListings" 
                   :key="`listing-${item.id}-${index}`" 
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
            <div v-if="hasMoreListings" class="view-all-button">
              <router-link to="/real-estate" class="view-all-link">
                Смотреть все объявления ({{ totalListings }})
              </router-link>
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
import HeroBanner from '../components/HeroBanner.vue';
import ImageGallery from '../components/ImageGallery.vue';
import ListingDetailsModal from '../components/ListingDetailsModal.vue';

export default {
  name: 'Home',
  components: {
    HeroBanner,
    ImageGallery,
    ListingDetailsModal,
  },
  // Используем как props, так и inject для максимальной совместимости
  props: {
    listings: {
      type: Array,
      default: () => []
    }
  },
  inject: {
    // Используем inject как fallback
    injectedListings: {
      from: 'listings',
      default: () => () => []
    },
    isLoading: {
      from: 'isLoading',
      default: () => () => false
    }
  },
  data() {
    return {
      selectedListing: null,
    };
  },
  computed: {
    // Получаем данные из props или inject
    currentListings() {
      // Сначала пробуем props, потом inject
      if (this.listings && this.listings.length > 0) {
        return this.listings;
      }
      
      // Если inject это функция, вызываем её
      if (typeof this.injectedListings === 'function') {
        return this.injectedListings();
      }
      
      return this.injectedListings || [];
    },
    
    recentListings() {
      // Возвращаем 5 последних объявлений
      const listings = this.currentListings;
      return listings.slice(0, 6);
    },
    
    totalListings() {
      return this.currentListings.length;
    },
    
    hasMoreListings() {
      // Проверяем, есть ли еще объявления помимо показанных
      return this.currentListings.length > 5;
    },
    
    isLoadingData() {
      if (typeof this.isLoading === 'function') {
        return this.isLoading();
      }
      return this.isLoading;
    }
  },
  // Добавляем watchers для отслеживания изменений
  // watch: {
  //   listings: {
  //     handler(newVal) {Current listings computed changed
  //       console.log('Listings changed in Home:', newVal);
  //     },
  //     deep: true,
  //     immediate: true
  //   },
  //   currentListings: {
  //     handler(newVal) {
  //       console.log('Current listings computed changed:', newVal);
  //     },
  //     deep: true,
  //     immediate: true
  //   }
  // },
  // mounted() {
  //   console.log('Home component mounted, listings:', this.currentListings);
  // },
  methods: {
    formatPrice(price) {
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
.home {
  min-height: 100vh;
}

.content-wrapper {
  padding-top: 70px;
}

main {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.listings-container {
  max-width: 100%;
  margin: 0;
  padding: 4rem 0;
  position: relative;
  background-color: #f8f9fa;
}

.listings-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  scroll-margin-top: 90px;
}

.listings-container h2 {
  margin-bottom: 4rem;
  color: #2c3e50;
  font-size: 2.8rem;
  text-align: center;
  font-weight: 600;
}

.loading-message {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #666;
}

.no-listings {
  text-align: center;
  padding: 2rem;
  font-size: 1.1rem;
  color: #666;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.details-button, .edit-button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.details-button {
  background-color: #3498db;
  color: white;
}

.details-button:hover {
  background-color: #2980b9;
}

.edit-button {
  background-color: #f8f9fa;
  color: #2c3e50;
  border: 1px solid #e0e0e0;
}

.edit-button:hover {
  background-color: #e9ecef;
}

.view-all-button {
  text-align: center;
  margin-top: 2rem;
}

.view-all-link {
  display: inline-block;
  padding: 1rem 2rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 500;
  transition: background-color 0.3s ease;
}

.view-all-link:hover {
  background-color: #2980b9;
}

.about-company {
  max-width: 100%;
  margin: 0;
  padding: 4rem 0;
  position: relative;
  background-color: #ffffff;
}

.about-company::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 4px;
  background: #3498db;
  border-radius: 2px;
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  scroll-margin-top: 90px;
}

.about-content h2 {
  margin-bottom: 4rem;
  color: #2c3e50;
  font-size: 2.8rem;
  text-align: center;
  font-weight: 600;
}

.about-content > p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #34495e;
  margin-bottom: 2rem;
}

.company-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.feature {
  text-align: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.2s;
}

.feature:hover {
  transform: translateY(-5px);
}

.feature h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.feature p {
  color: #7f8c8d;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .view-all-link {
    width: 100%;
    text-align: center;
  }
  
  .listings-grid {
    grid-template-columns: 1fr;
  }
  
  .card-actions {
    flex-direction: column;
  }
}
</style>