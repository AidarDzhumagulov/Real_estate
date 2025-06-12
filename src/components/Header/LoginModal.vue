<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <button class="close-btn" @click="$emit('close')">×</button>
      <h2>Вход в систему</h2>
      <form @submit.prevent="submitLogin">
        <label>
          email:
          <input type="email" v-model="email" required />
        </label>
        <label>
          Пароль:
          <input type="password" v-model="password" required />
        </label>
        <button type="submit">Войти</button>
      </form>
    </div>
  </div>
</template>

<script>
import { loginUser } from '../../api/auth';

export default {
  name: 'LoginModal',
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
        console.log('Ответ сервера:', response.data);

        if (response.data?.access_token) {
          localStorage.setItem('authToken', response.data.access_token);
          localStorage.setItem('userEmail', this.email);
          this.$emit('user-logged-in', { email: this.email });
        }

        window.dispatchEvent(new Event('user-logged-in'));
        this.$emit('close');
      } catch (error) {
        console.error('Ошибка входа:', error);
        console.error('Ответ сервера:', error.response?.data);
        alert('Ошибка входа: ' + (error.response?.data?.detail || error.response?.data || 'Проверьте данные'));
      } finally {
        this.isLoading = false;
      }
    }
  },
};
</script>

<style src="../../styles/loginModal.css"></style>