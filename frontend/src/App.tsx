import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/Home";
import CreditCheckPage from "./pages/creditCheck";
import InsertGradFile from "./pages/insertGradFile";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/creditcheck" element={<CreditCheckPage />} />
        <Route path="/insertgradfile" element={<InsertGradFile />} />
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </Router>
  );
};

export default App;
