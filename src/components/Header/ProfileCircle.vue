<template>
  <div class="profile-circle" @click="toggleProfile">
    <div class="circle">
      <span v-if="initials">{{ initials }}</span>
      <img v-else-if="userImage" :src="userImage" alt="Profile" class="profile-image" />
      <i v-else class="dx-icon dx-icon-account"></i>
    </div>
    <div v-if="showProfile" class="profile-dropdown">
      <div class="profile-info">
        <div class="user-name">{{ userName }}</div>
        <div class="user-email">{{ userEmail }}</div>
      </div>
      <div class="profile-actions">
        <button @click="goToProfile">Профиль</button>
        <button @click="logout">Выйти</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileCircle',
  data() {
    return {
      showProfile: false,
      userName: localStorage.getItem('userEmail')?.split('@')[0] || 'Пользователь',
      userEmail: localStorage.getItem('userEmail') || '',
      userImage: '',
      isAuthenticated: !!localStorage.getItem('authToken')
    };
  },
  methods: {
    toggleProfile() {
      this.showProfile = !this.showProfile;
    },
    goToProfile() {
      this.$router.push('/profile');
      this.showProfile = false;
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      this.$router.push('/login');
      this.showProfile = false;
      this.userName = '';
      this.userEmail = '';
      this.isAuthenticated = false;
    }
  },
  watch: {
    '$route'() {
      this.isAuthenticated = !!localStorage.getItem('authToken');
      console.log(localStorage.getItem('authToken'))
      this.userName = localStorage.getItem('userEmail')?.split('@')[0] || 'Пользователь';
      this.userEmail = localStorage.getItem('userEmail') || '';
    }
  },
  computed: {
    initials() {
      if (!this.userName) return '';
      return this.userName.split(' ').map(name => name[0].toUpperCase()).join('');
    },
  },
  methods: {
    toggleProfile() {
      this.showProfile = !this.showProfile;
    },
    goToProfile() {
      this.$router.push('/profile');
      this.showProfile = false;
    },
    logout() {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      this.$emit('logout');
      this.showProfile = false;
    },
    updateUserInfo() {
      const email = localStorage.getItem('userEmail');
      if (email) {
        this.userEmail = email;
        // Здесь можно добавить API-запрос для получения информации о пользователе
        this.userName = email.split('@')[0];
        this.userImage = '';
      } else {
        this.userEmail = '';
        this.userName = '';
        this.userImage = '';
      }
    }
  },
  created() {
    this.updateUserInfo();
    // Слушаем события входа/выхода
    window.addEventListener('user-logged-in', () => {
      this.updateUserInfo();
      this.$forceUpdate();
    });
    window.addEventListener('user-logged-out', () => {
      this.userEmail = '';
      this.userName = '';
      this.userImage = '';
      this.$forceUpdate();
    });
  },
  beforeUnmount() {
    window.removeEventListener('user-logged-in', () => {
      this.updateUserInfo();
      this.$forceUpdate();
    });
    window.removeEventListener('user-logged-out', () => {
      this.userEmail = '';
      this.userName = '';
      this.userImage = '';
      this.$forceUpdate();
    });
  },
  watch: {
    userEmail: {
      immediate: true,
      handler(newEmail) {
        if (newEmail) {
          this.updateUserInfo();
        }
      }
    }
  },
};
</script>

<style scoped>
.profile-circle {
  position: relative;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
}

.circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #2c3e50;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  position: relative;
  transition: all 0.3s ease;
}

.circle:hover {
  background-color: #34495e;
  transform: scale(1.1);
}

.profile-image {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.profile-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  min-width: 200px;
  z-index: 1000;
}

.profile-info {
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.user-name {
  font-size: 1.1rem;
  font-weight: 500;
  color: #2c3e50;
}

.user-email {
  font-size: 0.9rem;
  color: #666;
}

.profile-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
}

.profile-actions button {
  flex: 1;
  padding: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background: #ecf0f1;
  color: #2c3e50;
  font-weight: 500;
}

.profile-actions button:hover {
  background: #dcdde1;
}
</style>
