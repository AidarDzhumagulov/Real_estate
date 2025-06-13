<template>
  <div ref="profileCircle" class="profile-circle" @click="toggleProfile">
    <div class="circle">
      <span v-if="initials">{{ initials }}</span>
      <img v-else-if="userImage" :src="userImage" alt="Profile" class="profile-image" />
      <i v-else class="dx-icon dx-icon-account"></i>
    </div>
    <div v-if="showProfile" class="profile-dropdown">
      <div class="profile-info">
        <div class="user-fullname">{{ userFullName }}</div>
        <div class="user-email">{{ userEmail }}</div>
      </div>
      <div class="profile-actions">
        <button @click="goToProfile">Профиль</button>
        <button @click="logout" class="logout-btn">Выйти</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'ProfileCircle',
  setup() {
    const router = useRouter();
    const showProfile = ref(false);
    const profileCircle = ref(null);

    const userFullName = ref(localStorage.getItem('userFullName') || 'Пользователь');
    const userEmail = ref(localStorage.getItem('userEmail') || '');
    const userImage = ref('');

    const initials = computed(() => {
      if (!userFullName.value) return '';
      return userFullName.value
        .split(' ')
        .map(name => name[0].toUpperCase())
        .join('');
    });

    const toggleProfile = () => {
      showProfile.value = !showProfile.value;
    };

    const closeProfile = () => {
      showProfile.value = false;
    };

    const handleClickOutside = (event) => {
      if (profileCircle.value && !profileCircle.value.contains(event.target)) {
        closeProfile();
      }
    };

    const updateUserInfo = () => {
      const email = localStorage.getItem('userEmail');
      const fullName = localStorage.getItem('userFullName');
      if (email) {
        userEmail.value = email;
        userFullName.value = fullName || email.split('@')[0];
        userImage.value = '';
      } else {
        userEmail.value = '';
        userFullName.value = '';
        userImage.value = '';
      }
    };

    const goToProfile = () => {
      router.push('/profile');
      closeProfile();
    };

    const logout = () => {
      localStorage.removeItem('authToken');
      localStorage.removeItem('userEmail');
      localStorage.removeItem('userFullName');
      updateUserInfo();
      closeProfile();
      router.push('/');
    };

    onMounted(() => {
      updateUserInfo();
      document.addEventListener('click', handleClickOutside);
    });

    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside);
    });

    return {
      showProfile,
      userFullName,
      userEmail,
      userImage,
      initials,
      toggleProfile,
      goToProfile,
      logout,
      profileCircle
    };
  }
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
  background-color: #e67e22;
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

.user-fullname {
  font-size: 1.1rem;
  font-weight: 500;
  color: #2c3e50;
  margin-bottom: 0.3rem;
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

.logout-btn {
  background: #e74c3c !important;
  color: white !important;
}

.logout-btn:hover {
  background: #c0392b !important;
}
</style>
