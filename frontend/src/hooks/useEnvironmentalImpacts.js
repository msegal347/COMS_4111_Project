import { useState, useEffect } from 'react';
import { getEnvironmentalImpacts } from '../services/api';

const useEnvironmentalImpacts = () => {
  const [environmentalImpacts, setEnvironmentalImpacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchEnvironmentalImpacts = async () => {
      setLoading(true);
      try {
        const response = await getEnvironmentalImpacts();
        setEnvironmentalImpacts(response.data);
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchEnvironmentalImpacts();
  }, []);

  return { environmentalImpacts, loading, error };
};

export default useEnvironmentalImpacts;
