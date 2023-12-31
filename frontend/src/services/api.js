import axios from 'axios';

//const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://34.86.7.158:5000';

export const getMaterials = async filters => {
  const queryString = new URLSearchParams(filters).toString();
  return axios.get(`${API_BASE_URL}/api/material?${queryString}`);
};

export const getIndustrialApplications = async filters => {
  const queryString = new URLSearchParams(filters).toString();
  return axios.get(`${API_BASE_URL}/api/industrial?${queryString}`);
};

export const getGeneralCategories = async () => {
  return axios.get(`${API_BASE_URL}/api/general_categories/`);
};

export const getCompanies = async () => {
  return axios.get(`${API_BASE_URL}/api/company/`);
};

export const getEnvironmentalImpacts = async () => {
  return axios.get(`${API_BASE_URL}/api/environmental/`);
};

export const getSoldByRelations = async () => {
  return axios.get(`${API_BASE_URL}/api/sold_by/`);
};

export const executeQuery = async queryKey => {
  return axios.post(
    `${API_BASE_URL}/api/execute-query`,
    { query_key: queryKey },
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
};

export const postQuery = async filterData => {
  return axios.post(`${API_BASE_URL}/api/query`, filterData, {
    headers: {
      'Content-Type': 'application/json',
    },
  });
};
