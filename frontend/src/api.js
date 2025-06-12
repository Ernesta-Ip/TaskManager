import axios from 'axios';

// const token = localStorage.getItem('authToken');

export const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  withCredentials: true,
});