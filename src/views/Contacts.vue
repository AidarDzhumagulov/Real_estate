<template>
  <div class="contacts-page">
    <div class="content-wrapper">
      <div class="contacts">
        <div class="contacts-content">
          <h1>Контакты</h1>
          <div class="contact-info">
            <div class="contact-item">
              <h3>Адрес</h3>
              <p>г. Бишкек, ул. Киевская 77</p>
              <p>Бизнес-центр "Максимум", 3 этаж</p>
            </div>
            <div class="contact-item">
              <h3>Телефоны</h3>
              <p><a href="tel:+996555123456">+996 (555) 123-456</a></p>
              <p><a href="tel:+996700123456">+996 (700) 123-456</a></p>
            </div>
            <div class="contact-item">
              <h3>График работы</h3>
              <p>Пн-Пт: 9:00 - 18:00</p>
              <p>Сб: 10:00 - 15:00</p>
              <p>Вс: Выходной</p>
            </div>
            <div class="contact-item">
              <h3>Email</h3>
              <p><a href="mailto:info@kyrgyz-mulk.kg">info@kyrgyz-mulk.kg</a></p>
            </div>
          </div>
          <div class="contact-map">
            <iframe 
              src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2924.7732163657437!2d74.58743731547669!3d42.87661051077454!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x389ec81f4a0b9cd1%3A0x2c5c8b2d0a57d740!2z0YPQuy4g0JrQuNC10LLRgdC60LDRjywg0JHQuNGI0LrQtdC6!5e0!3m2!1sru!2skg!4v1635000000000!5m2!1sru!2skg" 
              width="100%" 
              height="400" 
              style="border:0;" 
              allowfullscreen="" 
              loading="lazy"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Contacts'
}
</script>

<style scoped>
.contacts-page {
  padding-top: 70px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.contacts {
  max-width: 100%;
  margin: 0;
  padding: 2rem 0;
  position: relative;
  background-color: #edf2f7;
}

h1 {
  margin-bottom: 3rem;
  color: #2c3e50;
  font-size: 2.8rem;
  text-align: center;
  font-weight: 600;
}

.contacts-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.contact-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.contact-item {
  padding: 1.5rem;
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.contact-item:hover {
  transform: translateY(-5px);
}

.contact-item h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.contact-item p {
  color: #7f8c8d;
  line-height: 1.5;
  margin-bottom: 0.5rem;
}

.contact-item a {
  color: #3498db;
  text-decoration: none;
  transition: color 0.2s;
}

.contact-item a:hover {
  color: #2980b9;
}

.contact-map {
  margin-top: 2rem;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.contact-map iframe {
  display: block;
  width: 100%;
  border-radius: 8px;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .contact-info {
    grid-template-columns: 1fr;
  }
}
</style> 