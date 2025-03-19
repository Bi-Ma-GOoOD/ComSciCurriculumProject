import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import OtpPage from './pages/OtpPage';
import SignUpPass from './pages/SignUpPass';
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