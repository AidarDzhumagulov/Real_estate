<template>
    <section class="hero-banner">
      <div class="overlay"></div>
      <div class="content">
        <h1>Найдите своё идеальное жильё в Кыргызстане с нами</h1>
        <p>Широкий выбор недвижимости, профессиональная помощь и гарантия безопасности сделки</p>
        <button @click="goToListings">Срочная продажа</button>
      </div>
    </section>
  </template>
  
  <script>
  import backgroundImage from '../assets/images/дом.jpg';

  export default {
    name: 'HeroBanner',
    data() {
      return {
        backgroundImage: `url(${backgroundImage})`
      }
    },
    methods: {
      goToListings() {
        const listingsSection = document.getElementById('listings');
        if (listingsSection) {
          const headerOffset = 80; // Высота шапки
          const elementPosition = listingsSection.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      },
    },
  };
  </script>

  <style scoped>
  .hero-banner {
    background-image: v-bind(backgroundImage);
  }
  </style>

  <style src="../styles/heroBanner.css"></style>