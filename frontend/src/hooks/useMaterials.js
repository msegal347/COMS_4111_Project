import { useState, useEffect } from 'react';
import { getMaterials } from '../services/api';

const useMaterials = () => {
  const [materials, setMaterials] = useState([]);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMaterials = async () => {
      setLoading(true);
      try {
        const response = await getMaterials(filters);
        setMaterials(response.data);
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchMaterials();
  }, [filters]); // Re-run this effect when filters change

  return { materials, filters, setFilters, loading, error };
};

export default useMaterials;
