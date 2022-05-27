import './App.css';
import Canvas from './Canvas';
import { Routes, Route } from 'react-router-dom';
import { Feedback } from './Feedback';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Canvas/>} />
        <Route path="/feedback" element={<Feedback/>} />
      </Routes>
    </div>
  );
}

export default App;
