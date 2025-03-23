// import React from 'react'
// import './LoginPage.css'
// import { useNavigate } from 'react-router-dom';

// function LoginPage() {
//   const navigate = useNavigate();

//   const handleSignUp = () => {
//     navigate('/SignUpPage');
//   };
//   return (
//     <div className='container'>
//       <div className="left-tab"></div>
//       <div className='content'>
//       <div className="ku-logo"></div>
//       <div className="bottom-tab"></div>
//       <div className='title'>KU ComSci Graduate’s Check</div>
//       </div>
//       <div className='login'>
//       <div className='title2'>เข้าสู่ระบบตรวจสอบหน่วยกิตและเช็คจบ</div>
//       <div className='email-title'>Email</div>
//       <input type="email" id="email" placeholder="abc@ku.th" className="email-input" />
//       <div className='password-title'>Password</div>
//       <input type="password" id="password" placeholder="1234abcd" className="password-input" />
//       <button className='signin-button'>เข้าสู่ระบบ</button>
//       <div className="link" onClick={handleSignUp}>สมัครสมาชิกด้วยบัญชีKU</div>
//       </div>
//       <div className="right-tab"></div>
//     </div>
//   );
// }

// export default LoginPage;

import React, { useState } from "react";
import "../styles/LoginPage.css";
import { useNavigate } from "react-router-dom";
import axios from "axios";

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSignUp = () => {
    navigate("/SignUpPage");
  };

  const handleLogin = async (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/login/", {
        email: email,
        password: password,
      });

      if (response.data.success) {
        let userId = response.data.user.id; // Assuming the user ID is returned in the response
        userId = userId.replace(/-/g, ""); // Remove "-" from the user_id
        localStorage.setItem("user", JSON.stringify(response.data.user)); // <--- ที่เพิ่มเข้ามา
        navigate("/insertGradFile", { state: { user_id: userId } }); // <--- ที่เพิ่มเข้ามา
      } else {
        setError(response.data.message);
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setError(error.response.data.message || "Login failed");
      } else {
        setError("Network error. Please try again later.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="left-tab"></div>
      <div className="content">
        <div className="ku-logo"></div>
        <div className="bottom-tab"></div>
        <div className="title">KU ComSci Graduate's Check</div>
      </div>
      <div className="login">
        <div className="title2">เข้าสู่ระบบตรวจสอบหน่วยกิตและเช็คจบ</div>

        {error && <div className="error-message">{error}</div>}

        <div className="email-title">Email</div>
        <input
          type="email"
          id="email"
          placeholder="abc@ku.th"
          className="email-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className="password-title">Password</div>
        <input
          type="password"
          id="password"
          placeholder="1234abcd"
          className="password-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          className="signin-button"
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? "กำลังเข้าสู่ระบบ..." : "เข้าสู่ระบบ"}
        </button>

        <div className="link" onClick={handleSignUp}>
          สมัครสมาชิกด้วยบัญชีKU
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
}

export default LoginPage;
