import React, { useState } from 'react';
import axios from 'axios';
import '../styles/QueryPage.css';

const QueryPage = () => {
  const [queryOptions, setQueryOptions] = useState({
    materials: {},
    companies: {},
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleCheckboxChange = (tableName, columnName) => {
    setQueryOptions(prev => ({
      ...prev,
      [tableName]: {
        ...prev[tableName],
        [columnName]: !prev[tableName][columnName],
      },
    }));
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('/api/query', queryOptions);
      setResults(response.data);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="query-page">
      <h1>Custom Query Builder</h1>
      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>Materials</legend>
          {/* Repeat for each column in the Materials table */}
          <label>
            <input
              type="checkbox"
              checked={!!queryOptions.materials.materialName}
              onChange={() => handleCheckboxChange('materials', 'materialName')}
            />
            Material Name
          </label>
          {/* ... other checkboxes */}
        </fieldset>
        {/* Repeat for other tables */}
        <fieldset>
          <legend>Companies</legend>
          {/* Repeat for each column in the Companies table */}
          <label>
            <input
              type="checkbox"
              checked={!!queryOptions.companies.companyName}
              onChange={() => handleCheckboxChange('companies', 'companyName')}
            />
            Company Name
          </label>
          {/* ... other checkboxes */}
        </fieldset>
        {/* Add more fieldsets for other tables */}
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Run Query'}
        </button>
      </form>
      <div className="results">
        {error && <div className="error">Error: {error.message}</div>}
        {results && (
          <div className="results-display">
            <h2>Results:</h2>
            <pre>{JSON.stringify(results, null, 2)}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default QueryPage;
