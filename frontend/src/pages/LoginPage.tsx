import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Swal from 'sweetalert2';
import '../styles/LoginPage.css';

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignUp = () => {
    navigate('/SignUpPage');
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    if (!email.trim() || !password.trim()) {
      Swal.fire({
        title: "ไม่สามารถเข้าสู่ระบบได้",
        text: "กรุณาระบุ Email และ Password",
        icon: "warning",
        confirmButtonText: "OK",
        confirmButtonColor: "#B2BB1E" 
      });
      setLoading(false);
      return;

    }

    
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email,
        password
      });

      if (response.data.success) {
        Swal.fire({
          title: "เข้าสู่ระบบสำเร็จ!",
          text: "ยินดีต้อนรับเข้าสู่ระบบ",
          icon: "success",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E",
        });

        // เก็บข้อมูล user ลง localStorage
        let userId = response.data.user.id;
        userId = userId.replace(/-/g, "");
        localStorage.setItem('user', JSON.stringify(response.data.user));

        
        navigate("/insertGradFile", { state: { user_id: userId } });
      } else {
        
        Swal.fire({
          title: "เข้าสู่ระบบไม่สำเร็จ",
          text: "Email หรือ รหัสผ่านไม่ถูกต้อง",
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E",
        });
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error) && error.response) {
      if (error.response.data.message.includes('Email not registered')) {
        Swal.fire({
          title: "Email ยังไม่ได้ลงทะเบียน",
          text: "กรุณาตรวจสอบ Email ของคุณใหม่",
          icon: "warning",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E",
        });
      } else {
        Swal.fire({
          title: "เข้าสู่ระบบไม่สำเร็จ",
          text: "Email หรือ Password ไม่ถูกต้อง",
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E",
        });
      }
    } else {
      Swal.fire({
        title: "ข้อผิดพลาด!",
        text: "ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์ กรุณาลองใหม่",
        icon: "error",
        confirmButtonText: "OK",
        confirmButtonColor: "#B2BB1E",
      });
    }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='container'>
      <div className="left-tab"></div>
      <div className='content'>
        <div className="ku-logo"></div>
        <div className="bottom-tab"></div>
        <div className='title'>KU ComSci Graduate's Check</div>
      </div>
      <div className='login'>
        <div className='title2'>เข้าสู่ระบบตรวจสอบหน่วยกิตและเช็คจบ</div>


        <div className='email-title'>Email</div>
        <input 
          type="email" 
          id="email" 
          placeholder="abc@ku.th" 
          className="email-input"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className='password-title'>Password</div>
        <input 
          type="password" 
          id="password" 
          placeholder="1234abcd" 
          className="password-input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button 
          className='signin-button' 
          onClick={handleLogin}
          disabled={loading}
        >
          {loading ? 'เข้าสู่ระบบ' : 'เข้าสู่ระบบ'}
        </button>

        <div className="link" onClick={handleSignUp}>สมัครสมาชิกด้วยบัญชีKU</div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
}

export default LoginPage;
