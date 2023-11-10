import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // Assuming you have a CSS file for global styles
import App from './app'; // Import the main App component
import ErrorBoundary from './ErrorBoundary';

// If you're using React Router, BrowserRouter can be set up here
//import { BrowserRouter as Router } from 'react-router-dom';

// If you're using Redux, the Provider can be set up here
// import { Provider } from 'react-redux';
// import store from './store'; // Import the store you configure

ReactDOM.render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
  document.getElementById('root')
);
