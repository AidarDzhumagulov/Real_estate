import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import RealEstate from '../views/RealEstate.vue';
import Contacts from '../views/Contacts.vue';
import About from '../views/About.vue';
import UserProfile from '../components/UserProfile.vue';
import Login from '../views/Login.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/real-estate',
    name: 'RealEstate',
    component: RealEstate
  },
  {
    path: '/contacts',
    name: 'Contacts',
    component: Contacts
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/profile',
    name: 'Profile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 80 // Учитываем высоту шапки
      };
    }
    return { top: 0 };
  }
});

// Проверка авторизации
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const isAuthenticated = localStorage.getItem('authToken');

  if (requiresAuth && !isAuthenticated) {
    next('/login');
  } else if (!requiresAuth && isAuthenticated && to.path === '/login') {
    next('/profile');
  } else {
    next();
  }
});

export default router; 