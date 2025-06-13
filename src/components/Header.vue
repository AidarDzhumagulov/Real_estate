<template>
  <header class="header">
    <div class="container">
      <div class="logo-wrapper">
        <router-link to="/" class="logo">Кыргыз Мүлк</router-link>
      </div>
      
      <!-- Кнопка мобильного меню -->
      <button class="mobile-menu-btn mobile-only" @click="isMenuOpen = !isMenuOpen">
        <span class="menu-icon"></span>
      </button>

      <!-- Навигация -->
      <nav class="nav" :class="{ 'nav-open': isMenuOpen }" aria-label="Основное меню сайта">
        <ul class="nav-list">
          <li>
            <router-link 
              to="/" 
              class="nav-link" 
              @click="handleNavClick"
            >
              Главная
            </router-link>
          </li>
          <li>
            <router-link to="/real-estate" class="nav-link" @click="handleNavClick">
              Недвижимость
            </router-link>
          </li>
          <li>
            <router-link to="/about" class="nav-link" @click="handleNavClick">
              О компании
            </router-link>
          </li>
          <li>
            <router-link to="/contacts" class="nav-link" @click="handleNavClick">
              Контакты
            </router-link>
          </li>
        </ul>
      </nav>

      <div class="actions">
        <AddButton @click="$emit('open-add')" />

        <ProfileCircle 
          v-if="isAuthenticated" 
          @logout="handleLogout" 
          ref="profileCircle"
        />
        <template v-else>
          <LoginButton @click="$emit('open-login')" />
          <RegisterButton @click="$emit('open-register')" />
        </template>
      </div>
    </div>
  </header>
</template>

<script>
import AddButton from './Header/Addbutton.vue';
import ProfileCircle from './Header/ProfileCircle.vue';
import LoginButton from './Header/LoginButton.vue';
import RegisterButton from './Header/RegisterButton.vue';

export default {
  name: "Header",
  components: {
    AddButton,
    ProfileCircle,
    LoginButton,
    RegisterButton,
  },
  data() {
    return {
      isAuthenticated: false,
      isMenuOpen: false
    };
  },
  methods: {
    handleLogin(userData) {
      this.isAuthenticated = true;
      localStorage.setItem('authToken', userData.token);
      localStorage.setItem('userEmail', userData.email);
      localStorage.setItem('userFullName', userData.fullName);
      window.dispatchEvent(new Event('user-logged-in'));
    },
    handleLogout() {
      this.isAuthenticated = false;
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userFullName');
      window.dispatchEvent(new Event('user-logged-out'));
    },
    checkAuth() {
      this.isAuthenticated = !!localStorage.getItem('authToken');
    },
    handleNavClick() {
      this.scrollToTop();
      this.isMenuOpen = false;
    },
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  },
  mounted() {
    this.checkAuth();
    window.addEventListener('user-logged-in', this.checkAuth);
    window.addEventListener('user-logged-out', this.checkAuth);
  },
  beforeUnmount() {
    window.removeEventListener('user-logged-in', this.checkAuth);
    window.removeEventListener('user-logged-out', this.checkAuth);
  }
};
</script>

<style>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(44, 62, 80, 0.98);
  padding: 0;
  z-index: 1000;
  backdrop-filter: blur(5px);
  height: var(--header-height);
  display: flex;
  align-items: center;
  margin: 0;
  width: 100%;
}

.container {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding-left: var(--container-padding);
  padding-right: var(--container-padding);
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  position: relative;
}

.logo-wrapper {
  flex: 0 0 auto;
  z-index: 1001;
  margin-right: 1rem;
}

.logo {
  color: #ecf0f1;
  font-size: clamp(1.2rem, 2vw, 1.5rem);
  font-weight: bold;
  text-decoration: none;
  padding: 0.5rem 0;
  display: block;
  white-space: nowrap;
}

.nav {
  flex: 1;
  display: flex;
  justify-content: center;
  margin: 0 1rem;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 1.5rem;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-size: 1rem;
  padding: 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #3498db;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
}

.menu-icon {
  display: block;
  width: 25px;
  height: 2px;
  background-color: #ecf0f1;
  position: relative;
  transition: background-color 0.3s ease;
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #ecf0f1;
  transition: transform 0.3s ease;
}

.menu-icon::before {
  transform: translateY(-8px);
}

.menu-icon::after {
  transform: translateY(8px);
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }

  .nav {
    position: fixed;
    top: var(--header-height);
    left: 0;
    right: 0;
    background: rgba(44, 62, 80, 0.98);
    padding: 1rem;
    transform: translateY(-100%);
    transition: transform 0.3s ease;
    z-index: 999;
  }

  .nav-open {
    transform: translateY(0);
  }

  .nav-list {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .actions {
    margin-left: auto;
  }
}
</style>
