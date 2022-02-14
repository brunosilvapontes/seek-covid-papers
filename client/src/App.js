import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  // Navigate,
} from 'react-router-dom';

import SeekPapers from './components/SeekPapers';
import Bookmark from './components/Bookmark';

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route exact path='/' element={ <SeekPapers/> } />
          <Route path='/bookmark' element={ <Bookmark/> } />
          {/* <Navigate to='/' /> */}
        </Routes>
      </Router>
    </>
  );
}

export default App;
