import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/QueryPage.css';

const QueryPage = () => {
  const [generalCategories, setGeneralCategories] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [generalResponse, companyResponse] = await Promise.all([
          axios.get('http://localhost:5000/api/general_categories'),
          axios.get('http://localhost:5000/api/company'),
        ]);
        setGeneralCategories(generalResponse.data);
        setCompanies(companyResponse.data);
      } catch (err) {
        setError('Failed to fetch data: ' + err.message);
        console.error('Failed to fetch data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleCategoryChange = event => {
    setSelectedCategory(event.target.value);
  };

  const handleCompanyChange = event => {
    setSelectedCompany(event.target.value);
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const filterData = {
        category: selectedCategory,
        company: selectedCompany,
      };
      const response = await axios.post('http://localhost:5000/api/query', filterData);
      setResults(response.data);
    } catch (err) {
      setError('Error during form submission: ' + err.message);
      console.error('Error during form submission:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="query-page">
      <h1>Custom Query Builder</h1>
      <form onSubmit={handleSubmit}>
        <div className="filters-container">
          <fieldset className="filter-section">
            <legend>Material General Category</legend>
            {generalCategories.map(category => (
              <div key={category.generalcategoryid} className="checkbox-container">
                <label>
                  <input
                    type="radio"
                    name="category"
                    value={category.categoryname}
                    checked={selectedCategory === category.categoryname}
                    onChange={handleCategoryChange}
                  />
                  {category.categoryname}
                </label>
              </div>
            ))}
          </fieldset>

          <fieldset className="filter-section">
            <legend>Companies</legend>
            {companies.map(company => (
              <div key={company.id} className="checkbox-container">
                <label>
                  <input
                    type="radio"
                    name="company"
                    value={company.name}
                    checked={selectedCompany === company.name}
                    onChange={handleCompanyChange}
                  />
                  {company.name}
                </label>
              </div>
            ))}
          </fieldset>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Run Query'}
        </button>
      </form>
      <div className="results-display">
        {error && <div className="error">Error: {error}</div>}
        <h2>Results:</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="results-content">
            {results.length > 0 ? (
              results.map((result, index) => (
                <div key={index} className="result-item">
                  <div>
                    <strong>Category Name:</strong> {result.categoryname}
                  </div>
                  <div>
                    <strong>Material Name:</strong> {result.materialname}
                  </div>
                  <div>
                    <strong>Company Name:</strong> {result.companyname}
                  </div>
                </div>
              ))
            ) : (
              <div>No results found.</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default QueryPage;
