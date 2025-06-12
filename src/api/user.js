import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';


export async function getUser(token) {
  const formData = new FormData();
  formData.append();

  const response = await axios.get(`${API_BASE_URL}/users/`, formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });

  return response.data.id;
}
