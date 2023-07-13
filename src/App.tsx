import React, { useEffect } from 'react';
import axios from 'axios';

function App() {
  useEffect(() => {
    // Make an API request to the backend server
    axios.post('/api/upload', { data: 'example data' })
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  return (
    <div className="App">
      <h1>Jellyfin-Library-Manager</h1>
      {/* Add your frontend components here */}
    </div>
  );
}

export default App;

