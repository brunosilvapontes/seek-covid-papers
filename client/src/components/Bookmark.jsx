import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Bookmark = () => {
  const [bookmarks, setBookmarks] = useState([]);
  const host = 'http://localhost:5000';

  useEffect(() => {
    axios.get(`${host}/bookmark`)
      .then(response => {
        setBookmarks(response.data);
      })
      .catch(() => alert('Fail to fetch bookmarks'))
  }, []);

  return (
    <div>
      <nav>
        <ul>
          <li>
            <Link to="/">Seek papers</Link>
          </li>
        </ul>
      </nav>
      <h1>Bookmarks:</h1>
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
          {bookmarks && bookmarks.length ? bookmarks.map((bookmark, key) => (
            <tr key={key}>
              <td>{bookmark.title}</td>
              <td>{bookmark.publish_time}</td>
              <td>{bookmark.journal}</td>
              <td>{bookmark.authors}</td>
              <td>{bookmark.url}</td>
            </tr>
          )) : ''}
        </tbody>
      </table>
    </div>
  );
};

export default Bookmark;
