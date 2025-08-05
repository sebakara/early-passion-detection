import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: '/api/v1', // Use relative path for proxy
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API functions
export const loginUser = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await api.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  // Get user info after successful login
  const userResponse = await api.get('/auth/me');
  
  return {
    access_token: response.data.access_token,
    user: userResponse.data,
  };
};

export const registerUser = async (userData) => {
  console.log('API: Registering user with data:', userData);
  
  try {
    const response = await api.post('/auth/register', userData);
    console.log('API: Registration response:', response.data);
    
    // Return the user data directly from registration response
    return {
      access_token: null, // No token needed for registration
      user: response.data,
    };
  } catch (error) {
    console.error('API: Registration error:', error);
    console.error('API: Error response:', error.response);
    throw error;
  }
};

export const logoutUser = async () => {
  try {
    await api.post('/auth/logout');
  } catch (error) {
    // Ignore logout errors
    console.log('Logout error:', error);
  }
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me');
  return response.data;
};

export const refreshToken = async () => {
  const response = await api.post('/auth/refresh');
  return response.data;
};

export default api; 