<template>
  <button class="add-button" @click="$emit('click')">Добавить объявление</button>
</template>

<script>
export default {
  name: "AddButton",
};
</script>

<style scoped>
.add-button {
  background-color: #27ae60;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 1rem;
}

.add-button:hover {
  background-color: #219a52;
}
</style>