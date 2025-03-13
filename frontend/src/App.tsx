import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import SignUpPage from './components/SignUpPage';
import OtpPage from './components/OtpPage';
import SignUpPass from './components/SignUpPass';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/SignUpPage" element={<SignUpPage />} />
        <Route path="/OtpPage" element={<OtpPage />} />
       <Route path="/SignUpPass" element={<SignUpPass />} />
      </Routes>
    </Router>
  );
}

export default App;