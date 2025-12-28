import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch }) {
  const [location, setLocation] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(location);
  };

  const handleChange = (e) => {
    setLocation(e.target.value);
  };

  return (
    <form className="search-bar" onSubmit={handleSubmit}>
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="Enter city name (e.g., Delhi, New York, Beijing)..."
          value={location}
          onChange={handleChange}
        />
        <button type="submit" className="search-button">
          🔍 Search
        </button>
      </div>
    </form>
  );
}

export default SearchBar;
