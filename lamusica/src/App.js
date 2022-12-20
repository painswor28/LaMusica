import './App.css';
import Navbar from './components/Navbar';
import React, { Component } from 'react';
import Home from './pages/Home';
//import Search from './pages/Search';
//import Recommend from './pages/Recommend';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <Router>
        <div class="container p-3 my-3">
          <div class="row">
            <div class="col-md-12">
              <Navbar />
            </div>
          </div>
          <Routes>
            <Route path="/" exact element={<Home />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
