import React, { useState, useEffect } from 'react';
import axios from 'axios';

const QUERY_TEMPLATES = {
  select_materials_by_category: 'Materials by Category',
  select_company_by_name: 'Company by Name',
  select_materials_by_property_range: 'Materials by Property Range',
  select_applications_by_material_id: 'Applications by Material ID',
  select_materials_by_tensile_strength: 'Materials by Tensile Strength',
  select_materials_and_companies: 'Materials and Companies',
  select_companies_in_industry: 'Companies in Industry',
  // ... more queries as needed
};

const ExecuteQueryPage = () => {
  const [queryKey, setQueryKey] = useState('select_materials_by_category');
  const [parameters, setParameters] = useState({});
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [generalCategories, setGeneralCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/general_categories');
        setGeneralCategories(response.data);
      } catch (err) {
        setError('Failed to fetch categories: ' + err.message);
        console.error('Failed to fetch categories:', err);
      }
    };

    fetchCategories();
  }, []);

  const handleChange = e => {
    const { name, value } = e.target;
    setParameters(prevParams => ({
      ...prevParams,
      [name]: value,
    }));
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      query_key: queryKey, // This should match the keys in the QUERY_TEMPLATES on the server
      parameters: parameters, // Make sure this is structured correctly as expected by the server
    };

    try {
      const response = await axios.post('http://localhost:5000/api/execute-query', payload, {
        headers: {
          'Content-Type': 'application/json', // Ensure the correct content type is set
        },
      });
      setResults(response.data);
    } catch (err) {
      setError('Error executing query: ' + err.message);
      console.error('Error executing query:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Execute SQL Query</h1>
      <form onSubmit={handleSubmit}>
        {/* Dropdown to select query template */}
        <select value={queryKey} onChange={e => setQueryKey(e.target.value)}>
          {Object.keys(QUERY_TEMPLATES).map(key => (
            <option key={key} value={key}>
              {QUERY_TEMPLATES[key]}
            </option>
          ))}
        </select>

        {/* Dropdown to select categories if needed for the selected query */}
        {queryKey === 'select_materials_by_category' && (
          <select name="category" value={parameters.category || ''} onChange={handleChange}>
            <option value="">Select a Category</option>
            {generalCategories.map(category => (
              <option key={category.generalcategoryid} value={category.categoryname}>
                {category.categoryname}
              </option>
            ))}
          </select>
        )}

        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Execute Query'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {results.length > 0 && (
        <table>
          <thead>
            <tr>
              {/* Dynamic table headers based on result keys */}
              {Object.keys(results[0]).map(key => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index}>
                {Object.values(result).map((value, idx) => (
                  <td key={idx}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ExecuteQueryPage;
