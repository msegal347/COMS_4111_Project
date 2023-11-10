import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';

export const getMaterials = async filters => {
  // Convert filters object to a query string
  const queryString = new URLSearchParams(filters).toString();
  return axios.get(`${API_BASE_URL}/api/material?${queryString}`);
};
