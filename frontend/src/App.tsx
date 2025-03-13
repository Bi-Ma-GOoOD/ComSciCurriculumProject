import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import SignUpPage from './components/SignUpPage';
import OtpPage from './components/OtpPage';
import SignUpPass from './components/SignUpPass';
import CreditCheckPage from "./pages/creditCheck";
import InsertGradFile from "./pages/insertGradFile";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/SignUpPage" element={<SignUpPage />} />
        <Route path="/OtpPage" element={<OtpPage />} />
       <Route path="/SignUpPass" element={<SignUpPass />} />
        <Route path="/creditcheck" element={<CreditCheckPage />} />
        <Route path="/insertgradfile" element={<InsertGradFile />} />
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </Router>
  );
}

export default App;