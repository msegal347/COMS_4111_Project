import { useState } from 'react';
import { addSoldBy } from '../services/api';

const useUpdateSoldBy = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const updateSoldBy = async ({ materialName, companyName, basePrice, currency }) => {
    setLoading(true);
    setError(null);
    setSuccess(false);
    try {
      // Construct the payload to send material and company names instead of IDs
      const payload = {
        materialName,
        companyName,
        basePrice,
        currency,
      };

      const response = await addSoldBy(payload); // Ensure the endpoint matches your backend route

      if (response.status === 200) {
        setSuccess(true);
      } else {
        setError('Failed to update sold by information');
      }
    } catch (err) {
      // Log the full error and set the error message for the user
      console.error('Update Sold By Error:', err);
      setError(err.response?.data?.error || 'An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return { updateSoldBy, loading, error, success };
};

export default useUpdateSoldBy;
