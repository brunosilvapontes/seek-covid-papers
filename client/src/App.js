// import logo from './logo.svg';
import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [papers, setPapers] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const host = 'http://localhost:5000';

  useEffect(() => {}, [papers]);

  const fetchPapers = async () => {
    try {
      if (!searchTerm) return;
      const response = await axios.get(`${host}/search?search_term=${searchTerm}`);
      if (!response || !response.data) return;
      setPapers(response.data);
    } catch (err) {
      const errMsg = err.response && err.response.data && err.response.data.message 
        ? err.response.data.message
        : err.message;
      alert(errMsg);
    }
  };

  const handleSearchTermChange = (event) => {
    const value = String(event.target.value);
    setSearchTerm(value);
  };

  return (
    <div className="App">
      <h1>Search for papers' metadata</h1>
      <div>
        <label>
          Search term: <input type="text" onChange={handleSearchTermChange} />
        </label>
        <button onClick={fetchPapers}>Search</button>
        <p>
          Hint: You can search for papers by the publish date typing a date in the following format: 2021-11-02 <br/>
          or type a text search term and we'll try to find papers based on title, journal, authors and abstract metadata. <br/>
        </p>
      </div>
      <h2>Found papers (API may limit the returned papers)</h2>
      <p>Total number of papers that contains the search term: {papers && papers.number_results ? papers.number_results : '0'}</p>
      <table>
        <thead>
          <tr>
            <th>TITLE</th>
            <th>PUBLISH DATE</th>
            <th>JOURNAL</th>
            <th>AUTHORS</th>
            <th>LINK</th>
          </tr>
        </thead>
        <tbody>
          {papers && papers.papers && papers.papers.length ? papers.papers.map((foundPaper, key) => (
            <tr key={key}>
              <td>{foundPaper.title}</td>
              <td>{foundPaper.publish_time}</td>
              <td>{foundPaper.journal}</td>
              <td>{foundPaper.authors}</td>
              <td>{foundPaper.url}</td>
            </tr>
          )) : ''}
        </tbody>
      </table>
    </div>
  );
}

export default App;
