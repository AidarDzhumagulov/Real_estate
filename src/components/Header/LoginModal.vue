<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2>Вход в систему</h2>
      <form @submit.prevent="submitLogin">
        <label>
          Email:
          <input type="email" v-model="email" required />
        </label>
        <label>
          Пароль:
          <input type="password" v-model="password" required />
        </label>
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { loginUser } from '../../api/auth';

export default {
  name: 'LoginModal',
  emits: ['close', 'login-success'],
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
    };
  },
  methods: {
    async submitLogin() {
      this.isLoading = true;
      try {
        const payload = {
          email: this.email,
          password: this.password
        };

        const response = await loginUser(payload);

        if (response.data?.access_token) {
          const userData = {
            token: response.data.access_token,
            email: this.email,
            fullName: response.data.full_name || this.email.split('@')[0]
          };

          // Сохраняем данные в localStorage
          localStorage.setItem('authToken', userData.token);
          localStorage.setItem('userEmail', userData.email);
          localStorage.setItem('userFullName', userData.fullName);

          
          // Передаем событие родительскому компоненту (App.vue)
          this.$emit('login-success', userData);
          
        } else {
          throw new Error('Не получен токен от сервера');
        }
      } catch (error) {
        alert('Ошибка входа: ' + (error.response?.data?.detail || error.response?.data || 'Проверьте данные'));
      } finally {
        this.isLoading = false;
      }
    }
  },
};
</script>

<style src="../../styles/loginModal.css"></style>