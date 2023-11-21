import { useState } from 'react';
import { postCustomQuery } from '../services/api';

const useCustomQuery = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runCustomQuery = async filters => {
    setLoading(true);
    setError(null);

    try {
      const response = await postCustomQuery(filters);
      setResults(response.data);
    } catch (err) {
      setError('Error executing custom query: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return { results, runCustomQuery, loading, error };
};

export default useCustomQuery;
