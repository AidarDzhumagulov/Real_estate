<template>
  <div class="about-page">
    <div class="content-wrapper">
      <div class="about-company">
        <div class="about-content">
          <h1>О компании</h1>
          <div class="about-text">
            <p>Кыргыз Мүлк — ваш надёжный и опытный партнёр в сфере недвижимости. Мы предлагаем полный спектр профессиональных услуг по продаже, покупке и аренде жилой, коммерческой и загородной недвижимости на территории всей Кыргызской Республики. Наша команда экспертов обладает глубоким знанием рынка и индивидуальным подходом к каждому клиенту, что позволяет находить оптимальные решения в кратчайшие сроки.</p>

            <p>С нами вы можете быть уверены в прозрачности сделок, юридической безопасности и высоком уровне сервиса. Независимо от того, ищете ли вы уютную квартиру, коммерческое помещение для бизнеса или участок земли для строительства — мы поможем вам найти именно то, что соответствует вашим целям и ожиданиям.</p>

            <p>Доверьте вопросы недвижимости профессионалам — выберите Кыргыз Мүлк и откройте для себя новые возможности на рынке жилья в Кыргызстане.</p>
          </div>

          <div class="company-features">
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-chart-line"></i>
              </div>
              <h3>Опыт</h3>
              <p>Многолетний опыт работы на рынке недвижимости</p>
            </div>
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-shield-alt"></i>
              </div>
              <h3>Надежность</h3>
              <p>Гарантия безопасности и прозрачности сделок</p>
            </div>
            <div class="feature">
              <div class="feature-icon">
                <i class="fas fa-users"></i>
              </div>
              <h3>Профессионализм</h3>
              <p>Команда квалифицированных специалистов</p>
            </div>
          </div>

          <div class="about-stats">
            <div class="stat-item">
              <h4>1000+</h4>
              <p>Успешных сделок</p>
            </div>
            <div class="stat-item">
              <h4>500+</h4>
              <p>Довольных клиентов</p>
            </div>
            <div class="stat-item">
              <h4>10+</h4>
              <p>Лет на рынке</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-page {
  padding-top: 70px;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.about-company {
  max-width: 100%;
  margin: 0;
  padding: 2rem 0;
  position: relative;
  background-color: #ffffff;
}

h1 {
  margin-bottom: 3rem;
  color: #2c3e50;
  font-size: 2.8rem;
  text-align: center;
  font-weight: 600;
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.about-text {
  max-width: 800px;
  margin: 0 auto 4rem;
}

.about-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #34495e;
  margin-bottom: 1.5rem;
}

.company-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature {
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feature:hover {
  transform: translateY(-10px);
}

.feature-icon {
  font-size: 2.5rem;
  color: #3498db;
  margin-bottom: 1.5rem;
}

.feature h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature p {
  color: #7f8c8d;
  line-height: 1.6;
}

.about-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-top: 4rem;
  text-align: center;
}

.stat-item {
  padding: 2rem;
  background: #3498db;
  color: white;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
}

.stat-item h4 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.stat-item p {
  font-size: 1.1rem;
  opacity: 0.9;
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
  }
  
  .about-text p {
    font-size: 1rem;
    line-height: 1.6;
  }
  
  .company-features {
    grid-template-columns: 1fr;
  }
  
  .about-stats {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}
</style> 