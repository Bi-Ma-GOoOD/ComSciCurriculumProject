import React, { useState } from 'react';
import '../styles/SignUpPage.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Swal from 'sweetalert2';

function SignUpPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');


  const handleNext = async () => {
    // Validate email
    if (!email.trim()) {
      Swal.fire({
        title: "ไม่สามารถลงทะเบียนได้",
        text: "กรุณาระบุ Email",
        icon: "warning",
        confirmButtonText: "OK",
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/api/signup/', { email: email.trim() });
      console.log(response.data); // เช็ค response ที่ได้รับจาก backend

      if (response.data.success) {
    
        Swal.fire({
          title: "ลงทะเบียนสำเร็จ",
          text: "คุณได้ลงทะเบียนสำเร็จแล้ว",
          icon: "success",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        }).then(() => {
          localStorage.setItem('signupReference', response.data.reference);
          localStorage.setItem('signupEmail', email.trim());
          navigate('/OtpPage', { state: { email: email.trim() } });
        });
      } else if (response.data.message === "Email already exists") {
        
        Swal.fire({
          title: "อีเมลนี้มีอยู่ในระบบแล้ว",
          text: "กรุณาใช้อีเมลอื่น",
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        });
      } else {
        Swal.fire({
          title: "เกิดข้อผิดพลาด",
          text: response.data.message || 'Signup failed',
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        });
      }
    } catch (err) {
      console.error(err);
      if (axios.isAxiosError(err)) {
        Swal.fire({
          title: "เกิดข้อผิดพลาด",
          text: err.response?.data?.message || 'Signup failed',
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        });
      } else {
        Swal.fire({
          title: "เกิดข้อผิดพลาด",
          text: 'Signup failed',
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        });
      }
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

      <div className='signup-page'>
        <div className='title2'>ลงทะเบียนตรวจสอบหน่วยกิตและเช็คจบ</div>
        <div className='email-title-signup'>Email (@ku)</div>
        
        <div className='input-container'>
          <input 
            type="email" 
            id="email" 
            placeholder="abc@ku.th" 
            className="email-input"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <button 
          className='next-signup-button' 
          onClick={handleNext}
        >
          ถัดไป
        </button>
      </div>

      <div className="right-tab"></div>
    </div>
  );
}

export default SignUpPage;