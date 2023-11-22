import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/execute-query">Execute Query</Link>
        </li>
        <li>
          <Link to="/custom-query">Custom Query</Link>
        </li>
        <li>
          <Link to="/update-database">Update Materials</Link>
        </li>
        <li>
          <Link to="/update-sold-by">Update Sold By</Link>
        </li>{' '}
      </ul>
    </nav>
  );
};

export default Navigation;
