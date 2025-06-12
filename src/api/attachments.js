import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export async function uploadImage(file, token) {
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await axios.post(`${API_BASE_URL}/attachments/`, formData, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'multipart/form-data'
    }
  });
  
  return response.data.id;
}

export async function loadAttachment(id, token) {
  try {
    // Сначала пробуем получить метаданные attachment
    const response = await axios.get(`${API_BASE_URL}/attachments/?id_=${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    
    return {
      id: response.data.id || id,
      filename: response.data.filename || `attachment_${id}`,
      url: `${API_BASE_URL}/attachments/?id_=${id}`,
      contentType: response.data.content_type,
      size: response.data.size,
      createdAt: response.data.created_at
    };
  } catch (error) {
    console.error(`Ошибка загрузки attachment ${id}:`, error);
    
    // Если первый способ не сработал, пробуем альтернативные endpoints
    const alternativeEndpoints = [
      `${API_BASE_URL}/attachments/${id}`,
      `${API_BASE_URL}/files/${id}`,
      `${API_BASE_URL}/attachments/download/${id}`
    ];
    
    for (const endpoint of alternativeEndpoints) {
      try {
        const altResponse = await axios.get(endpoint, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        return {
          id: id,
          filename: altResponse.data.filename || `attachment_${id}`,
          url: endpoint,
          contentType: altResponse.data.content_type || 'image/jpeg',
          size: altResponse.data.size || 0,
          createdAt: altResponse.data.created_at
        };
      } catch (altError) {
        console.error(`Ошибка загрузки через ${endpoint}:`, altError);
        continue;
      }
    }
    
    // Если все альтернативы не сработали, возвращаем базовый объект
    return {
      id: id,
      filename: `attachment_${id}`,
      url: `${API_BASE_URL}/attachments/?id_=${id}`,
      contentType: 'image/jpeg',
      size: 0,
      error: true
    };
  }
}

// Функция для загрузки нескольких attachments одновременно
export async function loadMultipleAttachments(attachmentIds, token) {
  const promises = attachmentIds.map(id => loadAttachment(id, token));
  
  try {
    const results = await Promise.allSettled(promises);
    
    // Возвращаем только успешно загруженные изображения
    return results
      .filter(result => result.status === 'fulfilled')
      .map(result => result.value);
  } catch (error) {
    console.error('Ошибка загрузки множественных attachments:', error);
    return [];
  }
}

// Функция для получения изображения как blob
export async function getImageAsBlob(attachmentId, token) {
  const endpoints = [
    `${API_BASE_URL}/attachments/?id_=${attachmentId}`,
    `${API_BASE_URL}/attachments/${attachmentId}`,
    `${API_BASE_URL}/files/${attachmentId}`,
    `${API_BASE_URL}/attachments/download/${attachmentId}`
  ];
  
  for (const endpoint of endpoints) {
    try {
      const response = await axios.get(endpoint, {
        headers: {
          Authorization: `Bearer ${token}`,
          Accept: 'image/*'
        },
        responseType: 'blob'
      });
      
      if (response.status === 200) {
        return response.data;
      }
    } catch (error) {
      console.error(`Ошибка загрузки blob через ${endpoint}:`, error);
      continue;
    }
  }
  
  throw new Error(`Не удалось загрузить изображение ${attachmentId}`);
}

// Функция для предварительной загрузки изображения (создание blob URL)
export async function preloadImage(attachmentId, token) {
  try {
    const blob = await getImageAsBlob(attachmentId, token);
    return URL.createObjectURL(blob);
  } catch (error) {
    console.error('Ошибка предварительной загрузки изображения:', error);
    return null;
  }
}

// Функция для получения прямой ссылки на изображение с токеном
export function getImageUrl(attachmentId, token) {
  return `${API_BASE_URL}/attachments/?id_=${attachmentId}&token=${encodeURIComponent(token)}`;
}

// Функция для проверки доступности attachment
export async function checkAttachmentAvailability(attachmentId, token) {
  const endpoints = [
    `${API_BASE_URL}/attachments/?id_=${attachmentId}`,
    `${API_BASE_URL}/attachments/${attachmentId}`,
    `${API_BASE_URL}/files/${attachmentId}`
  ];
  
  for (const endpoint of endpoints) {
    try {
      const response = await axios.head(endpoint, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      
      if (response.status === 200) {
        return { available: true, endpoint };
      }
    } catch (error) {
      continue;
    }
  }
  
  return { available: false, endpoint: null };
}