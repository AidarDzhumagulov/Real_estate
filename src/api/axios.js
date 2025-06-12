import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',  // здесь ваш бэкенд URL
  withCredentials: true, // если работаете с куками для авторизации
});

export default instance;
