<template>
  <button class="login-button" @click="$emit('click')">Войти</button>
</template>

<script>
export default {
  name: "LoginButton"
};
</script>

<style scoped>
.login-button {
  background-color: transparent;
  border: 2px solid #ecf0f1;
  color: #ecf0f1;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 0.5rem;
}

.login-button:hover {
  background-color: #ecf0f1;
  color: #2c3e50;
}
</style>