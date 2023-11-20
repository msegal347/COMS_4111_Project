import { useState } from 'react';
import { executeQuery } from '../services/api';

const useExecuteQuery = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runQuery = async queryKey => {
    setLoading(true);
    setError(null);

    try {
      const response = await executeQuery(queryKey);
      setResults(response.data);
    } catch (err) {
      setError('Error executing query: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return { results, runQuery, loading, error };
};

export default useExecuteQuery;
