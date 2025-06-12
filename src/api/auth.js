// src/api/auth.js
import axios from 'axios';
import instance from './axios';


const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  withCredentials: true,
  responseType: 'json'
});

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/api/users/register/', userData);
    return response.data;
  } catch (error) {
    console.error('Ошибка регистрации:', error.response?.data || error.message);
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/api/users/login/', credentials, {
      withCredentials: true
    });
    
    const { access_token } = response.data;
    if (access_token) {
      localStorage.setItem('authToken', access_token);
    }

      return response.data;
  } catch (error) {
    console.error('Ошибка входа:', error.response?.data || error.message);
    throw error;
  }
};

