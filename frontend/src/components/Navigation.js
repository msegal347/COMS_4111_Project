import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/query">Query</Link>
        </li>
        <li>
          <Link to="/materials">Materials</Link>
        </li>
        <li>
          <Link to="/industrial-applications">Industrial Applications</Link>
        </li>
        <li>
          <Link to="/general-categories">General Categories</Link>
        </li>
        <li>
          <Link to="/companies">Companies</Link>
        </li>
        <li>
          <Link to="/sold-by">Sold By</Link>
        </li>
        <li>
          <Link to="/environment">Environment</Link>
        </li>{' '}
        {/* Add this line for environment */}
        {/* Add other navigation links here */}
      </ul>
    </nav>
  );
};

export default Navigation;
