import { useState, useEffect } from 'react';
import { getIndustrialApplications } from '../services/api';

const useIndustrialApplications = () => {
  const [applications, setApplications] = useState([]);
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchApplications = async () => {
      setLoading(true);
      try {
        const response = await getIndustrialApplications(filters);
        setApplications(response.data);
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [filters]);

  return { applications, filters, setFilters, loading, error };
};

export default useIndustrialApplications;
