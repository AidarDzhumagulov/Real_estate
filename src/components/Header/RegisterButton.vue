<template>
  <button class="register-button" @click="$emit('click')">Регистрация</button>
</template>

<script>
export default {
  name: "RegisterButton",
};
</script>

<style scoped>
.register-button {
  background: transparent;
  border: 2px solid #3498db;
  color: #ecf0f1;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.register-button:hover {
  background: #3498db;
  color: white;
}
</style> 