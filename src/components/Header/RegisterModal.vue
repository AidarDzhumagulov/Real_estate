<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2>Регистрация</h2>
      <form @submit.prevent="submitRegister">
        <div class="form-group">
          <label>Имя:</label>
          <input 
            type="text" 
            v-model="formData.firstName" 
            required 
            placeholder="Введите имя"
          />
        </div>

        <div class="form-group">
          <label>Фамилия:</label>
          <input 
            type="text" 
            v-model="formData.lastName" 
            required 
            placeholder="Введите фамилию"
          />
        </div>

        <div class="form-group">
          <label>Email:</label>
          <input 
            type="email" 
            v-model="formData.email" 
            required 
            placeholder="example@mail.com"
          />
        </div>

        <div class="form-group">
          <label>Телефон:</label>
          <input 
            type="tel" 
            v-model="formData.phone" 
            required 
            placeholder="Введите номер телефона"
          />
        </div>

        <div class="form-group">
          <label>Пароль:</label>
          <input 
            type="password" 
            v-model="formData.password" 
            required 
            placeholder="Введите любой пароль"
          />
        </div>

        <div class="form-group">
          <label>Подтвердите пароль:</label>
          <input 
            type="password" 
            v-model="formData.confirmPassword" 
            required 
            placeholder="Повторите пароль"
          />
        </div>

        <button type="submit" class="submit-btn">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</template>

<script>
import { registerUser } from '../../api/auth';

export default {
  name: 'RegisterModal',
  data() {
    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: ''
      }
    }
  },
  methods: {
    async submitRegister() {
      if (this.formData.password !== this.formData.confirmPassword) {
        alert('Пароли не совпадают');
        return;
      }

      const payload = {
        email: this.formData.email,
        password: this.formData.password,
        first_name: this.formData.firstName,
        last_name: this.formData.lastName,
        phone_number: this.formData.phone
      };

      try {
        const result = await registerUser(payload);
        console.log('Успешная регистрация:', result);
        alert('Регистрация прошла успешно!');
        this.$emit('close');
      } catch (error) {
        console.error('Ошибка регистрации:', error.response?.data || error.message);
        alert('Ошибка при регистрации: ' + (error.response?.data?.detail || 'проверьте данные'));
      }
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
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
}

h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  text-align: center;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #2c3e50;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input:focus {
  border-color: #3498db;
  outline: none;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: #27ae60;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background: #219a52;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: 1.5rem;
  }
}
</style> 