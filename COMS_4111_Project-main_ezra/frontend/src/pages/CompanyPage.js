import React from 'react';
import useCompanies from '../hooks/useCompany';
import CompanyFilter from './CompanyFilter';
import CompanyTable from './CompanyTable';

const CompanyPage = () => {
  const { companies, loading, error } = useCompanies();

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <CompanyFilter onFilterChange={() => {}} />
      <CompanyTable companies={companies} />
    </div>
  );
};

export default CompanyPage;
