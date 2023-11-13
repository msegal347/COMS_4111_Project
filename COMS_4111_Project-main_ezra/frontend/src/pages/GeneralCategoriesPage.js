import React from 'react';
import useGeneralCategories from '../hooks/useGeneralCategories';
import GeneralCategoriesFilter from './GeneralCategoriesFilter';
import GeneralCategoriesTable from './GeneralCategoriesTable';

const GeneralCategoriesPage = () => {
  const { categories, setFilters, loading, error } = useGeneralCategories();

  const handleFilterChange = (filterName, value) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [filterName]: value,
    }));
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <GeneralCategoriesFilter onFilterChange={handleFilterChange} />
      <GeneralCategoriesTable categories={categories} />
    </div>
  );
};

export default GeneralCategoriesPage;
