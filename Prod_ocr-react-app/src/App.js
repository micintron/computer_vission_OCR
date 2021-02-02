import React from 'react';
import './App.scss';
import {
  BrowserRouter as Router,
  Route
} from "react-router-dom";

import PdfOcr from './pages/pdf-ocr/PdfOcr';
import PassportOcr from './pages/passport-ocr/PassportOcr';
import ImageOcr from './pages/image-ocr/ImageOcr';
import LicenseOcr from './pages/license-ocr/LicenseOcr';
import TextAnalysis from './pages/text-analysis/TextAnalysis';
import Sidebar from './views/sidebar/Sidebar';

function App() {

  return (

    <Router>

      <div className="app">

        <Sidebar />
        
        <div className="main-container">
            <Route path="/ocr/pdf" component={PdfOcr} /> 
            <Route path="/ocr/passport" component={PassportOcr} /> 
            <Route path="/ocr/image" component={ImageOcr} /> 
            <Route path="/ocr/license" component={LicenseOcr} /> 
            <Route path="/analysis/text" component={TextAnalysis} /> 
        </div>
      </div>

    </Router>
  );
}

export default App;
