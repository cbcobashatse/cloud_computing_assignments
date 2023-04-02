import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, BrowserRouter, Navigate } from 'react-router-dom';

import Search from './search.js';
import Upload from './upload.js';
import Home from './home.js';

function App() {
    return (
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="search_photos" element={<Search />} />
            <Route path="upload_photos" element={<Upload />} />
          </Routes>
        </BrowserRouter>
    );
}

export default App;
