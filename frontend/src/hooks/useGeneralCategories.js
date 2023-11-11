import { useState, useEffect } from 'react';
import { getGeneralCategories } from '../services/api'; // ensure you have this function defined in api.js

const useGeneralCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      setLoading(true);
      try {
        const response = await getGeneralCategories(); // Use the service function
        setCategories(response.data); // Assuming the API returns an array of categories
        setError(null);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []); // Empty dependency array means this effect will only run once after the initial render

  return { categories, loading, error };
};

export default useGeneralCategories;
