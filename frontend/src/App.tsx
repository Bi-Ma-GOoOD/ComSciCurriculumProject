import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SignUpPage from './pages/SignUpPage';
import OtpPage from './pages/OtpPage';
import SignUpPass from './pages/SignUpPass';
import CreditCheckPage from "./pages/creditCheck";
import InsertGradFile from "./pages/insertGradFile";
import FileAttachCheck from "./pages/fileAttachCheck";
import FileAttachList from "./pages/fileAttachList";

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
        <Route path="/fileattachcheck" element={<FileAttachCheck />}/>
        <Route path="/fileattachlist" element={<FileAttachList />} />
      </Routes>
    </Router>
  );
}

export default App;