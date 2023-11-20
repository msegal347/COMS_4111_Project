import React, { useState } from 'react';
import useQueryData from '../hooks/useQueryData';
import '../styles/QueryPage.css';

const QueryPage = () => {
  const {
    generalCategories,
    companies,
    industrialApplications,
    results,
    loading,
    error,
    submitQuery,
  } = useQueryData();

  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [selectedApplication, setSelectedApplication] = useState('');

  const handleCategoryChange = event => setSelectedCategory(event.target.value);
  const handleCompanyChange = event => setSelectedCompany(event.target.value);
  const handleApplicationChange = event => setSelectedApplication(event.target.value);

  const handleSubmit = event => {
    event.preventDefault();
    const filterData = {
      category: selectedCategory,
      company: selectedCompany,
      industrial: selectedApplication,
    };
    submitQuery(filterData);
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
                <option key={app.id} value={app.application_name}>
                  {app.application_name}
                </option>
              ))}
            </select>
            {error && <div className="error">{error}</div>}
          </fieldset>

          <button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Run Query'}
          </button>
        </form>
      </div>
      <div className="results-display">
        {error && <div className="error">Error: {error}</div>}
        {loading ? (
          <p>Loading...</p>
        ) : (
          <div className="results-content">
            {results.length > 0 ? (
              <table>
                <thead>
                  <tr>
                    <th>Material Name</th>
                    <th>Category Name</th>
                    <th>Company Name</th>
                    <th>Application Name</th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((result, index) => (
                    <tr key={result.materialname + index}>
                      <td>{result.materialname}</td>
                      <td>{result.categoryname}</td>
                      <td>{result.companyname}</td>
                      <td>{result.applicationname}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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
