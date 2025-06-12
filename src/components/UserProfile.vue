<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>Профиль пользователя</h1>
    </div>
    <div class="profile-content">
      <div class="profile-info">
        <div class="profile-section">
          <h2>Основная информация</h2>
          <div class="form-group">
            <label>Имя</label>
            <input v-model="profileData.firstName" type="text" class="form-input" />
          </div>
          <div class="form-group">
            <label>Фамилия</label>
            <input v-model="profileData.lastName" type="text" class="form-input" />
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="profileData.email" type="email" class="form-input" />
          </div>
        </div>
        <div class="profile-section">
          <h2>Контакты</h2>
          <div class="form-group">
            <label>Телефон</label>
            <input v-model="profileData.phone" type="tel" class="form-input" />
          </div>
        </div>
      </div>
      <div class="profile-actions">
        <button @click="save" :disabled="!isDataChanged" class="save-button">Сохранить</button>
        <button @click="cancel" :disabled="!isDataChanged" class="cancel-button">Отмена</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserProfile',
  data() {
    return {
      isLoading: true,
      profileData: {
        firstName: '',
        lastName: '',
        email: '',
        phone: ''
      },
      savedData: null,
      isDataChanged: false
    };
  },
  watch: {
    profileData: {
      handler() {
        this.dataChanged();
      },
      deep: true
    }
  },
  methods: {
    async loadProfile() {
      try {
        const response = await axios.get('http://localhost:8000/api/users/profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }
        });
        // Преобразование полей API в локальные
        this.profileData = {
          firstName: response.data.first_name || '',
          lastName: response.data.last_name || '',
          email: response.data.email || '',
          phone: response.data.phone_number || ''
        };
        this.savedData = { ...this.profileData };
      } catch (error) {
        console.error('Ошибка при загрузке профиля:', error);
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          this.$router.push('/login');
        }
      } finally {
        this.isLoading = false;
      }
    },
    dataChanged() {
      this.isDataChanged = JSON.stringify(this.profileData) !== JSON.stringify(this.savedData);
    },
    async save() {
      try {
        // Преобразуем локальные поля в формат API
        const payload = {
          first_name: this.profileData.firstName,
          last_name: this.profileData.lastName,
          email: this.profileData.email,
          phone_number: this.profileData.phone
        };
        await axios.patch('http://localhost:8000/api/users/profile', payload, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('authToken')}`
          }
        });
        this.savedData = { ...this.profileData };
        this.isDataChanged = false;
        alert('Профиль успешно сохранен');
      } catch (error) {
        console.error('Ошибка при сохранении профиля:', error);
        alert('Ошибка при сохранении профиля');
        if (error.response?.status === 401) {
          localStorage.removeItem('authToken');
          this.$router.push('/login');
        }
      }
    },
    cancel() {
      Object.assign(this.profileData, this.savedData);
      this.isDataChanged = false;
    }
  },
  created() {
    this.loadProfile();
  }
};
</script>

<style scoped>
/* твои стили оставляем без изменений */
.profile-page {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 2rem;
}

.profile-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile-section {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid #eee;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.profile-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.save-button,
.cancel-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button {
  background-color: #4a90e2;
  color: white;
}

.save-button:hover {
  background-color: #357abd;
}

.cancel-button {
  background-color: #f8f9fa;
  color: #666;
  border: 1px solid #ddd;
}

.cancel-button:hover {
  background-color: #e9ecef;
}

.save-button:disabled,
.cancel-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
