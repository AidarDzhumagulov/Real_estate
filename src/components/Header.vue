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

        <ProfileCircle @logout="logout" v-if="userEmail" />
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
      userEmail: localStorage.getItem('userEmail') || null,
      isMenuOpen: false
    };
  },
  watch: {
    '$store.state.user': {
      handler() {
        this.checkLogin();
      },
      immediate: true
    }
  },
  methods: {
    handleLogin(email) {
      this.userEmail = email;
      localStorage.setItem('userEmail', email);
      this.$forceUpdate();
    },
    checkLogin() {
      const token = localStorage.getItem('authToken');
      const email = localStorage.getItem('userEmail');
      if (token && email) {
        this.userEmail = email;
        this.$forceUpdate();
        // Обновляем ProfileCircle
        this.$nextTick(() => {
          const profileCircle = this.$refs.profileCircle;
          if (profileCircle) {
            profileCircle.updateUserInfo();
          }
        });
      } else {
        this.userEmail = null;
        this.$forceUpdate();
      }
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      this.userEmail = null;
      window.dispatchEvent(new Event('user-logged-out'));
      this.$forceUpdate();
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      this.userEmail = null;
      window.dispatchEvent(new Event('user-logged-out'));
      this.$forceUpdate();
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
    this.checkLogin();
    // слушаем события входа и выхода
    window.addEventListener('user-logged-in', () => {
      this.checkLogin();
      this.$forceUpdate();
    });
    window.addEventListener('user-logged-out', () => {
      this.checkLogin();
      this.$forceUpdate();
    });
  },
  beforeUnmount() {
    window.removeEventListener('user-logged-in', this.checkLogin);
    window.removeEventListener('user-logged-out', this.checkLogin);
  },
  mounted() {
    this.checkLogin();
    // слушаем события входа и выхода
    window.addEventListener('user-logged-in', () => {
      this.checkLogin();
      this.$forceUpdate(); // Принудительно обновляем компонент
    });
    window.addEventListener('user-logged-out', () => {
      this.checkLogin();
      this.$forceUpdate();
    });
  },
  beforeUnmount() {
    window.removeEventListener('user-logged-in', this.checkLogin);
    window.removeEventListener('user-logged-out', this.checkLogin);
  },
  methods: {
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    checkLogin() {
      const token = localStorage.getItem('authToken');
      const email = localStorage.getItem('userEmail');
      if (token && email) {
        this.userEmail = email;
      } else {
        this.userEmail = null;
      }
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      this.userEmail = null;
    },
    handleNavClick() {
      if (this.isMenuOpen) {
        this.isMenuOpen = false;
      }
      if (this.$route.path === '/') {
        this.scrollToTop();
      }
    }
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
  gap: 0.5rem;
  margin: 0;
  padding: 0;
  align-items: center;
}

.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  font-size: 0.9rem;
  display: inline-block;
  white-space: nowrap;
}

.nav-link:hover {
  color: #3498db;
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.actions {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex: 0 0 auto;
  z-index: 1001;
}

.logout-btn {
  background: transparent;
  color: white;
  border: 1px solid white;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.2s ease;
  white-space: nowrap;
  font-size: 0.9rem;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-email {
  color: white;
  font-size: 0.9rem;
  margin-right: 0.5rem;
  white-space: nowrap;
}

/* Мобильное меню */
.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  z-index: 1001;
  margin-left: auto;
}

.menu-icon {
  display: block;
  width: 24px;
  height: 2px;
  background-color: white;
  position: relative;
  transition: background-color 0.3s;
}

.menu-icon::before,
.menu-icon::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: white;
  transition: transform 0.3s;
}

.menu-icon::before {
  transform: translateY(-7px);
}

.menu-icon::after {
  transform: translateY(7px);
}

/* Мобильные стили */
@media (max-width: 768px) {
  .header {
    height: var(--header-height);
  }

  .container {
    padding-left: var(--container-padding);
    padding-right: var(--container-padding);
  }

  .mobile-menu-btn {
    display: block;
    padding: 0.5rem;
    margin-left: 1rem;
  }

  .nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(44, 62, 80, 0.98);
    margin: 0;
    padding: var(--header-height) var(--container-padding) var(--container-padding);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
    z-index: 1000;
  }

  .nav.nav-open {
    transform: translateX(0);
  }

  .nav-list {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    width: 100%;
  }

  .nav-link {
    font-size: 1.1rem;
    padding: 0.75rem;
    width: 100%;
  }

  .actions {
    gap: 0.5rem;
  }

  .user-email {
    display: none;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.1rem;
  }

  .actions {
    gap: 0.25rem;
  }

  .nav-link {
    font-size: 1rem;
  }
}

/* Анимация кнопки меню */
.nav-open .menu-icon {
  background-color: transparent;
}

.nav-open .menu-icon::before {
  transform: rotate(45deg);
}

.nav-open .menu-icon::after {
  transform: rotate(-45deg);
}
</style>
