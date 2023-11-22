import React, { useState } from 'react';
import useExecuteQuery from '../hooks/useExecuteQuery';
import '../styles/ExecuteQueryPage.css';

const QUERY_TEMPLATES = {
  select_all_materials: 'All Materials',
  select_all_companies: 'All Companies',
  select_all_general_categories: 'All General Categories',
  select_all_industrial_applications: 'All Industrial Applications',
  select_all_materials_by_company_3M: 'Materials Sold by Company 3M',
  select_all_materials_metals: 'All Metals',
  list_all_materials_with_applications_and_industries:
    'All Materials with Applications and Industries',
  list_materials_sold_by_all_companies: 'Materials Sold by All Companies',
  list_materials_used_in_pharmaceuticals_by_BASF: 'Materials Used in Pharmaceuticals Sold by BASF',
  list_toxic_materials_sold_by_international_paper: 'Toxic Materials Sold by International Paper',
  price_of_toxic_materials_with_tensile_strength_greater_than_100:
    'Price of Toxic Materials with Tensile Strength Greater than 100',
  list_materials_with_average_price: 'Materials with Average Price',
  top_5_most_toxic_materials: 'Top 5 Most Toxic Materials',
  materials_with_their_categories_and_number_of_industrial_applications:
    'Materials with Their Categories and Number of Industrial Applications',
  companies_and_count_of_materials_they_sell: 'Companies and Count of Materials They Sell',
  materials_not_sold_by_any_company: 'Materials Not Sold by Any Company',
  materials_with_high_carbon_footprint_and_environmental_impact:
    'Materials with High Carbon Footprint and Environmental Impact',
  materials_more_expensive_than_average_category_price:
    'Materials More Expensive than Average Category Price',
  companies_and_materials_they_sell_in_electronics_industry:
    'Companies and Materials They Sell in Electronics Industry',
  three_most_expensive_general_categories: 'Three Most Expensive General Categories',
  all_materials_and_their_environmental_impacts: 'All Materials and Their Environmental Impacts',
};

const ExecuteQueryPage = () => {
  const [queryKey, setQueryKey] = useState('select_all_materials');
  const { results, runQuery, loading, error } = useExecuteQuery();

  const handleSubmit = async event => {
    event.preventDefault();
    runQuery(queryKey);
  };

  return (
    <div className="execute-query-page">
      <h1>Execute SQL Query</h1>
      <form onSubmit={handleSubmit}>
        <select value={queryKey} onChange={e => setQueryKey(e.target.value)}>
          {Object.entries(QUERY_TEMPLATES).map(([key, value]) => (
            <option key={key} value={key}>
              {value}
            </option>
          ))}
        </select>
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Execute Query'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {results.length > 0 && (
        <table>
          <thead>
            <tr>
              {results.length > 0 && Object.keys(results[0]).map(key => <th key={key}>{key}</th>)}
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
