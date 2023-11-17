import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/QueryPage.css';

const QueryPage = () => {
  const [generalCategories, setGeneralCategories] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [industrialApplications, setIndustrialApplications] = useState([]);
  const [selectedApplication, setSelectedApplication] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [generalResponse, companyResponse, applicationResponse] = await Promise.all([
          axios.get('http://localhost:5000/api/general_categories'),
          axios.get('http://localhost:5000/api/company'),
          axios.get('http://localhost:5000/api/industrial'),
        ]);
        setGeneralCategories(generalResponse.data);
        setCompanies(companyResponse.data);
        setIndustrialApplications(applicationResponse.data);
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

  const handleApplicationChange = event => {
    setSelectedApplication(event.target.value);
  };

  const handleSubmit = async event => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const filterData = {
        category: selectedCategory,
        company: selectedCompany,
        industrial: selectedApplication,
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
    <div>
      <div className="query-page">
        <h1>Materials DB Custom Query</h1>
        <form onSubmit={handleSubmit} className="query-form">
          <fieldset>
            <legend>Material General Category</legend>
            <select name="category" onChange={handleCategoryChange} value={selectedCategory}>
              <option value="">Select a Category</option>
              {generalCategories.map(category => (
                <option key={category.generalcategoryid} value={category.categoryname}>
                  {category.categoryname}
                </option>
              ))}
            </select>
          </fieldset>

          <fieldset>
            <legend>Companies</legend>
            <select name="company" onChange={handleCompanyChange} value={selectedCompany}>
              <option value="">Select a Company</option>
              {companies.map(company => (
                <option key={company.id} value={company.name}>
                  {company.name}
                </option>
              ))}
            </select>
          </fieldset>

          <fieldset>
            <legend>Industrial Applications</legend>
            <select
              name="industrial"
              onChange={handleApplicationChange}
              value={selectedApplication}
            >
              <option value="">Select an Application</option>
              {industrialApplications.map(app => (
                <option key={app.applicationid} value={app.applicationname}>
                  {app.applicationname}
                </option>
              ))}
            </select>
          </fieldset>

          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Run Query'}
          </button>
        </form>
      </div>
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
                  <div>
                    <strong>Industrial Application:</strong> {result.applicationname}
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
