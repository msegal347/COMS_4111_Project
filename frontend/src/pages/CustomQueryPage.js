import React, { useState, useEffect } from 'react';
import useCustomQuery from '../hooks/useCustomQuery';
import { getGeneralCategories, getCompanies, getIndustrialApplications } from '../services/api';
import '../styles/CustomQueryPage.css';

const CustomQueryPage = () => {
  const [categories, setCategories] = useState([]);
  const [companies, setCompanies] = useState([]);
  const [applications, setApplications] = useState([]);

  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedCompany, setSelectedCompany] = useState('');
  const [selectedApplication, setSelectedApplication] = useState('');

  const { results, runCustomQuery, loading, error } = useCustomQuery();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const categoryResponse = await getGeneralCategories();
        const companyResponse = await getCompanies();
        const applicationResponse = await getIndustrialApplications();
        setCategories(categoryResponse.data);
        setCompanies(companyResponse.data);
        setApplications(applicationResponse.data);
      } catch (error) {
        console.error('Error fetching data', error);
      }
    };
    fetchData();
  }, []);

  const handleSubmit = async event => {
    event.preventDefault();
    console.log('Submitting query with filters:', {
      category: selectedCategory,
      company: selectedCompany,
      application: selectedApplication,
    });
    runCustomQuery({
      category: selectedCategory,
      company: selectedCompany,
      application: selectedApplication,
    });
  };

  useEffect(() => {
    if (results.query_results) {
      console.log('Query results:', results.query_results);
    }
  }, [results]);

  const renderTableRows = data => {
    console.log('Rendering table rows with data:', data);
    return data.map((result, index) => (
      <tr key={`result-${index}`}>
        <td>{result.materialname}</td>
        <td>{result.categoryname}</td>
        <td>{result.companyname}</td>
        <td>{result.applicationname}</td>
      </tr>
    ));
  };

  return (
    <div className="custom-query-page">
      <h1>Custom Query</h1>
      <form onSubmit={handleSubmit}>
        <fieldset>
          <legend>Material General Category</legend>
          <select value={selectedCategory} onChange={e => setSelectedCategory(e.target.value)}>
            <option value="">Select a Category</option>
            {categories.map(category => (
              <option key={category.generalcategoryid} value={category.categoryname}>
                {category.categoryname}
              </option>
            ))}
          </select>
        </fieldset>
        <fieldset>
          <legend>Companies</legend>
          <select value={selectedCompany} onChange={e => setSelectedCompany(e.target.value)}>
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
            value={selectedApplication}
            onChange={e => setSelectedApplication(e.target.value)}
          >
            <option value="">Select an Application</option>
            {applications.map(app => (
              <option key={app.id} value={app.application_name}>
                {app.application_name}
              </option>
            ))}
          </select>
        </fieldset>
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Run Custom Query'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {results.query_results && (
        <table>
          <thead>
            <tr>
              <th>Material Name</th>
              <th>Category</th>
              <th>Company</th>
              <th>Application</th>
            </tr>
          </thead>
          <tbody>{renderTableRows(results.query_results)}</tbody>
        </table>
      )}
    </div>
  );
};

export default CustomQueryPage;
