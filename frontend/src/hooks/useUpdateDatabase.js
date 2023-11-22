import { useState } from 'react';
import { addMaterial } from '../services/api';

const useUpdateDatabase = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const updateDatabase = async formData => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      const response = await addMaterial(formData);
      if (response.status === 201) {
        setSuccess(true);
      }
    } catch (err) {
      console.error(err.response.data);
      setError(err.response?.data?.error || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return { updateDatabase, loading, error, success };
};

export default useUpdateDatabase;
