import React from 'react';
import './LoadingSpinner.css';

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner" />
      <p>Loading pollution data...</p>
    </div>
  );
}

export default LoadingSpinner;
