import { useState, useEffect } from 'react';
import { getSoldByRelations } from '../services/api';

const useSoldBy = () => {
  const [soldByRelations, setSoldByRelations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSoldByRelations = async () => {
      setLoading(true);
      try {
        const response = await getSoldByRelations();
        setSoldByRelations(response.data);
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSoldByRelations();
  }, []);

  return { soldByRelations, loading, error };
};

export default useSoldBy;
