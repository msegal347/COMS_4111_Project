import React, { useState } from 'react';
import axios from 'axios';
import '../styles/QueryPage.css';

const QueryPage = () => {
  const [queryOptions, setQueryOptions] = useState({
    category: {},
    material: {},
    company: {},
    sold_by: {},
    environmental: {},
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFilterChange = (tableName, columnName, value) => {
    setQueryOptions(prev => ({
      ...prev,
      [tableName]: {
        ...prev[tableName],
        [columnName]: value,
      },
    }));
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/api/query', queryOptions);

      console.log('Response data:', response.data);

      if (response.data.length === 0) {
        console.log('Query returned no results.');
      }

      setResults(response.data);
    } catch (err) {
      console.error('QueryPage handleSubmit error:', err);
      setError(err.response ? err.response.data : err.message);
    } finally {
      setLoading(false);
    }
  };

  // Renders a text input for string filters
  const renderTextInput = (tableName, columnName) => (
    <label>
      {columnName.charAt(0).toUpperCase() + columnName.slice(1)}:
      <input
        type="text"
        value={queryOptions[tableName][columnName] || ''}
        onChange={e => handleFilterChange(tableName, columnName, e.target.value)}
      />
    </label>
  );

  // Renders a checkbox for boolean filters
  const renderCheckbox = (tableName, columnName) => (
    <label>
      <input
        type="checkbox"
        checked={!!queryOptions[tableName][columnName]}
        onChange={() =>
          handleFilterChange(tableName, columnName, !queryOptions[tableName][columnName])
        }
      />
      {columnName.charAt(0).toUpperCase() + columnName.slice(1)}
    </label>
  );

  return (
    <div className="query-page">
      <h1>Custom Query Builder</h1>
      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>Materials</legend>
          {renderTextInput('category', 'categoryName')}
          {/* Repeat for other filters as needed */}
        </fieldset>
        <fieldset>
          <legend>Materials</legend>
          {renderTextInput('material', 'materialname')}
          {/* Repeat for other filters as needed */}
        </fieldset>
        <fieldset>
          <legend>Companies</legend>
          {renderTextInput('company', 'companyname')}
          {/* Repeat for other filters as needed */}
        </fieldset>
        <fieldset>
          <legend>Sold By</legend>
          {renderCheckbox('sold_by', 'is_sold_by_company_a')}
          {/* Repeat for other filters as needed */}
        </fieldset>
        <fieldset>
          <legend>Environmental</legend>
          {renderCheckbox('environmental', 'recyclability')}
          {/* Repeat for other filters as needed */}
        </fieldset>
        {/* ... add more fields for additional tables */}
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Run Query'}
        </button>
      </form>
      <div className="results-display">
        {error && <div className="error">Error: {error}</div>}
        <h2>Results:</h2>
        <div className="results-content">
          {results.length > 0 ? (
            results.map((result, index) => (
              <div key={index} className="result-item">
                {/* Customize this part based on the result structure */}
                <div>
                  <strong>Category Name:</strong> {result.categoryname}
                </div>
                <div>
                  <strong>Material Name:</strong> {result.materialname}
                </div>
                <div>
                  <strong>Company Name:</strong> {result.companyname}
                </div>
                <div>
                  <strong>Recyclable:</strong> {result.recyclability ? 'Yes' : 'No'}
                </div>
                {/* Add more result fields here */}
              </div>
            ))
          ) : (
            <div>No results found.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default QueryPage;
