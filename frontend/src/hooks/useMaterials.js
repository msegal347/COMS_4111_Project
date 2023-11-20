import { useState, useCallback } from 'react';
import { getMaterials } from '../services/api';

const useMaterials = () => {
  const [materials, setMaterials] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchMaterials = useCallback(async category => {
    setLoading(true);
    setError(null);
    setMaterials([]);
    try {
      const filters = category ? { category: category } : {};
      console.log(`Requesting materials with category: ${category}`);
      const response = await getMaterials(filters);
      console.log('Received response:', response.data);
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
      const response = await getMaterials();
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
