<template>
  <div v-if="userEmail" class="user-profile">
    <span class="email-circle">{{ userEmail.charAt(0).toUpperCase() }}</span>
    <span class="email-text">{{ userEmail }}</span>
  </div>
  <button v-else class="login-button" @click="$emit('click')">Войти</button>
</template>

<script>
export default {
  name: "LoginButton",
  data() {
    return {
      userEmail: localStorage.getItem('userEmail') || ''
    };
  },
  watch: {
    '$store.state.userEmail': {
      handler(newEmail) {
        this.userEmail = newEmail;
      },
      immediate: true
    }
  }
};
</script>

<style scoped>
.email-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: #3498db;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  font-weight: bold;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.email-text {
  color: #ecf0f1;
  font-size: 14px;
}

.login-button {
  background-color: transparent;
  border: 2px solid #ecf0f1;
  color: #ecf0f1;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  background-color: #ecf0f1;
  color: #2c3e50;
}
</style>