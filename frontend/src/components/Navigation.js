import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/query">Search Database</Link>
        </li>
        <li>
          <Link to="/materials">Materials</Link>
        </li>
        <li>
          <Link to="/industrial-applications">Industrial Applications</Link>
        </li>
        <li>
          <Link to="/sold-by">Sold By</Link>
        </li>
        <li>
          <Link to="/environment">Environment</Link>
        </li>{' '}
      </ul>
    </nav>
  );
};

export default Navigation;
