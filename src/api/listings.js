import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';


// Создание объявления
export async function createListing(payload, token) {
  const response = await axios.post(`${API_BASE_URL}/listings/`, payload, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  return response.data;
}

export async function getListing(token) {
    const response = await axios.get(`${API_BASE_URL}/listings/`, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
    });

    return response.data;
}

export async function deleteListing(id_, token) {
    const response = await axios.delete(`${API_BASE_URL}/listings/?id_=${id_}`, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
    });

    return response.data;
}

export async function updateListing(id_, payload, token) {

    const response = await axios.patch(`${API_BASE_URL}/listings/${id_}`, payload, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });

    return response.data;
}
