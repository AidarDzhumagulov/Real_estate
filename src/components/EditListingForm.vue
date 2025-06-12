<template>
  <div class="edit-form-overlay">
    <div class="edit-form">
      <h3>Редактировать объявление</h3>
      <form @submit.prevent="submit">
        <div class="form-group">
          <label>Название</label>
          <input v-model="formData.title" type="text" required placeholder="Например: 2-комнатная квартира в центре" />
        </div>

        <div class="form-group">
          <label>Тип недвижимости</label>
          <select v-model="formData.propertyType" required>
            <option value="">Выберите тип</option>
            <option value="apartment">Квартира</option>
            <option value="house">Дом</option>
            <option value="commercial">Коммерческая недвижимость</option>
            <option value="land">Земельный участок</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Цена (сом)</label>
            <input v-model="formData.price" type="number" required placeholder="Введите цену" />
          </div>
          <div class="form-group">
            <label>Площадь (м²)</label>
            <input v-model="formData.area" type="number" placeholder="Введите площадь" />
          </div>
        </div>

        <div class="form-group">
          <label>Адрес</label>
          <input v-model="formData.address" type="text" required placeholder="Укажите адрес" />
        </div>

        <div class="form-group">
          <label>Описание</label>
          <textarea 
            v-model="formData.description" 
            required 
            rows="4" 
            placeholder="Подробное описание недвижимости"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn">Сохранить</button>
          <button type="button" @click="$emit('cancel')" class="cancel-btn">Отмена</button>
          <button type="button" @click="deleteListing" class="delete-btn">Удалить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EditListingForm',
  props: {
    listing: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      formData: {
        id: this.listing.id,
        title: this.listing.title || '',
        propertyType: this.listing.propertyType || this.listing.property_type || '',
        price: this.listing.price || 0,
        area: this.listing.area || 0,
        address: this.listing.address || '',
        description: this.listing.description || '',
        rooms: this.listing.rooms || 0,
        floor: this.listing.floor || 0,
      },
    };
  },
  methods: {
    submit() {
      if (this.validateForm()) {
        // Передаем данные с ID для обновления
        this.$emit('save', { ...this.formData });
      }
    },
    deleteListing() {
      this.$emit('delete', this.listing);
    },
    validateForm() {
      const required = [
        'title', 
        'propertyType', 
        'price', 
        'address', 
        'description'
      ];
      const isValid = required.every(field => {
        const value = this.formData[field];
        return value !== null && value !== undefined && value.toString().trim() !== '';
      });
      
      if (!isValid) {
        alert('Пожалуйста, заполните все обязательные поля');
        return false;
      }

      return true;
    }
  }
};
</script>

<style scoped>
.edit-form-overlay {
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

.edit-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  margin: auto;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.image-previews {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.preview-container {
  position: relative;
}

.preview-image {
  width: 100%;
  height: 100px;
  object-fit: cover;
  border-radius: 4px;
}

.remove-image {
  position: absolute;
  top: -8px;
  right: -8px;
  background: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn,
.cancel-btn,
.delete-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.submit-btn {
  background: #27ae60;
  color: white;
}

.cancel-btn {
  background: #95a5a6;
  color: white;
}

.delete-btn {
  background: #e74c3c;
  color: white;
  margin-left: auto;
}

.submit-btn:hover {
  background: #219a52;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.delete-btn:hover {
  background: #c0392b;
}
</style>