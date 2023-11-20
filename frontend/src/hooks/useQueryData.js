import { useState, useEffect } from 'react';
import {
  getGeneralCategories,
  getCompanies,
  getIndustrialApplications,
  postQuery,
} from '../services/api';

const useQueryData = () => {
  const [generalCategories, setGeneralCategories] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [industrialApplications, setIndustrialApplications] = useState([]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const [generalResponse, companyResponse, applicationResponse] = await Promise.all([
          getGeneralCategories(),
          getCompanies(),
          getIndustrialApplications(),
        ]);
        setGeneralCategories(generalResponse.data);
        setCompanies(companyResponse.data);
        setIndustrialApplications(applicationResponse.data);
      } catch (err) {
        setError('Failed to fetch data: ' + err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const submitQuery = async filterData => {
    setLoading(true);
    setError(null);

    try {
      const response = await postQuery(filterData);
      setResults(response.data);
    } catch (err) {
      setError('Error during form submission: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    generalCategories,
    companies,
    industrialApplications,
    results,
    loading,
    error,
    submitQuery,
  };
};

export default useQueryData;
