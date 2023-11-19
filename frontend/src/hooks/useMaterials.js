import { useState, useCallback } from 'react';
import axios from 'axios';

const useMaterials = () => {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMaterials = useCallback(async category => {
    setLoading(true);
    setError(null);
    setMaterials([]);
    try {
      const queryString = category ? `category=${encodeURIComponent(category)}` : '';
      console.log(`Requesting materials with category: ${category}`); // Log the exact request
      const response = await axios.get(`http://localhost:5000/api/query/materials?${queryString}`);
      console.log('Received response:', response.data); // Log the received response
      setMaterials(response.data);
    } catch (err) {
      console.error('Error fetching materials:', err);
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAllMaterials = useCallback(async () => {
    setLoading(true);
    setError(null);
    setMaterials([]);
    try {
      const response = await axios.get('http://localhost:5000/api/material');
      setMaterials(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  return { materials, fetchMaterials, fetchAllMaterials, loading, error };
};

export default useMaterials;
