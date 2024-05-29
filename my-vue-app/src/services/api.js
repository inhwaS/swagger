import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Your API base URL
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Utility function to convert an object to FormData
function getFormData(object) {
  const formData = new FormData();
  Object.keys(object).forEach(key => formData.append(key, object[key]));
  return formData;
}

// Updated login function
export async function login(username, password) {
  const data = getFormData({ username, password });
  try {
    const response = await axios.post('http://localhost:8000/token', data, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    console.log(response);
    return response;
  } catch (error) {
    console.error('Login error', error.response);
    throw error;
  }
}

export async function getCurrentUser(token) {
  try {
    const response = await axios.get('http://localhost:8000/users/me', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching current user:', error.response);
    throw error;
  }
}

export default {
  login,
  getCurrentUser,
  // Add other endpoints here as needed
};
