import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import '../styles/SignUpPass.css';
import Swal from 'sweetalert2';

function SignUpPass() {
  const navigate = useNavigate();
  const location = useLocation();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    role: 'Roles',
    studentCode: '',
    keyCode: '',
    name: ''  
  });
  
  const [isOpen, setIsOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const roles = ["นิสิต", "ผู้ตรวจสอบหลักฐาน"];
  
  // Load email from previous step
  useEffect(() => {
    const storedEmail = localStorage.getItem('signupEmail');
    
    if (storedEmail) {
      setFormData(prev => ({ ...prev, email: storedEmail }));
    } else if (location.state?.email) {
      setFormData(prev => ({ ...prev, email: location.state.email }));
      localStorage.setItem('signupEmail', location.state.email);
    } else {
      Swal.fire({
        title: 'Email ไม่ถูกต้อง',
        text: 'กรุณาเริ่มกระบวนการลงทะเบียนใหม่',
        icon: 'error',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      })
    }
  }, [location]);
  
  // Get placeholder based on selected role
  const getPlaceholder = () => {
    if (formData.role === "นิสิต") {
      return "รหัสนิสิต";
    } else if (formData.role === "ผู้ตรวจสอบหลักฐาน") {
      return "key";
    }
    return "";
  };
  
  // Handle field changes
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };
  
  // Handle role selection
  const handleRoleSelect = (role: string) => {
    setFormData(prev => ({ ...prev, role, studentCode: '', keyCode: '' }));
    setIsOpen(false);
  };
  
  // Handle code/key input based on role
  const handleCodeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (formData.role === "นิสิต") {
      setFormData(prev => ({ ...prev, studentCode: value }));
    } else if (formData.role === "ผู้ตรวจสอบหลักฐาน") {
      setFormData(prev => ({ ...prev, keyCode: value }));
    }
  };
  
  // Submit registration
  const handleRegister = async () => {
    
    // Validate form
    if (!formData.email) {
      Swal.fire({
        title: 'กรุณากรอก Email',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    
    if (!formData.password) {
      Swal.fire({
        title: 'กรุณากรอกรหัสผ่าน',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      Swal.fire({
        title: 'กรุณากรอกรหัสผ่านให้ตรงกัน',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    
    if (formData.role === 'Roles') {
      Swal.fire({
        title: 'กรุณาเลือก Role',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    
    if (formData.role === "นิสิต" && !formData.studentCode) {
      Swal.fire({
        title: 'กรุณากรอกรหัสนิสิต',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }

    if (formData.role === "นิสิต") {
      const studentCodeRegex = /^[0-9]{10}$/;
      if (!studentCodeRegex.test(formData.studentCode)) {
        Swal.fire({
          title: 'รหัสนิสิตไม่ถูกต้อง',
          text: 'รหัสนิสิตต้องเป็นตัวเลข 10 หลัก',
          icon: 'warning',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        });
        return;
      }
    }
    
    if (formData.role === "ผู้ตรวจสอบหลักฐาน" && !formData.keyCode) {
      Swal.fire({
        title: 'กรุณากรอก Key Code',
        icon: 'warning',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/register/', {
        email: formData.email,
        password: formData.password,
        confirmPassword: formData.confirmPassword,
        role: formData.role,
        studentCode: formData.studentCode,
        keyCode: formData.keyCode,
        name: formData.name || 'User'  // Default name if not provided
      });
      
      if (response.data.success) {
        // Clear localStorage
        localStorage.removeItem('signupEmail');
        localStorage.removeItem('signupReference');
        
        Swal.fire({
          title: 'ลงทะเบียนสำเร็จ!',
          icon: 'success',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        }).then(() => {
          // Redirect to login page
          navigate('/');
        });
      }
    } catch (err) {
      if (axios.isAxiosError(err)) {
      if (err.response?.data?.message?.includes('Student code already exists')) {
        Swal.fire({
          title: 'รหัสนิสิตนี้ถูกใช้งานแล้ว',
          text: 'กรุณาตรวจสอบรหัสนิสิตใหม่อีกครั้ง',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        });
      } else if (err.response?.data?.message?.includes('Invalid key code')) {
        Swal.fire({
          title: 'Key ไม่ถูกต้อง',
          text: 'กรุณาตรวจสอบ Key ใหม่อีกครั้ง',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        });
      } else if (err.response?.data?.message?.includes('Password must be between 8 and 18 characters long')) {
        Swal.fire({
          title: 'กรุณากรอกรหัสผ่านใหม่',
          text: 'รหัสผ่านต้องมีความยาวระหว่าง 8-18 ตัวอักษร',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        })
      } else if (err.response?.data?.message?.includes('Password can only contain english letters, numbers, and special characters')) {
        Swal.fire({
          title: 'กรุณากรอกรหัสผ่านใหม่',
          text: 'รหัสผ่านต้องประกอบด้วยตัวอักษรภาษาอังกฤษ ตัวเลข และอักขระพิเศษเท่านั้น',
          icon: 'error',
          confirmButtonText: 'OK',
          confirmButtonColor: "#B2BB1E"
        })
      }
    } else {
      Swal.fire({
        title: 'เกิดข้อผิดพลาด',
        text: 'ไม่สามารถลงทะเบียนได้ กรุณาลองใหม่อีกครั้ง',
        icon: 'error',
        confirmButtonText: 'OK',
        confirmButtonColor: "#B2BB1E"
      });
    }
    } finally {
      setIsSubmitting(false);
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
      <div className='signup-password'>
        <div className='title2'>ลงทะเบียนตรวจสอบหน่วยกิตและเช็คจบ</div>
        
        <div className='password-title'>Password</div>
        <input 
          type="password" 
          id="password" 
          placeholder="1234abcd" 
          className="password-input"
          value={formData.password}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        
        <div className='confirm-password-title'>Confirm Password</div>
        <input 
          type="password" 
          id="confirmPassword" 
          placeholder="1234abcd" 
          className="confirm-password-input"
          value={formData.confirmPassword}
          onChange={handleChange}
          disabled={isSubmitting}
        />
        
        <div className="input-group">
          <div className="dropdown-container">
            <button 
              className="dropdown-button" 
              onClick={() => setIsOpen(!isOpen)}
              disabled={isSubmitting}
            >
              <span>{formData.role}</span>
              <span className="dropdown-icon">▼</span>
            </button>
            {isOpen && (
              <ul className="dropdown-menu">
                {roles.map((option) => (
                  <li key={option} onClick={() => handleRoleSelect(option)}>
                    {option}
                  </li>
                ))}
              </ul>
            )}
          </div>
          
          <input 
            type="text" 
            className="id-student-input" 
            placeholder={getPlaceholder()}
            value={formData.role === "นิสิต" ? formData.studentCode : formData.keyCode}
            onChange={handleCodeChange}
            disabled={isSubmitting || formData.role === 'Roles'}
          />
        </div>
        
        
        <button 
          className='register-button'
          onClick={handleRegister}
          disabled={isSubmitting}
        >
          {isSubmitting ? 'กำลังสมัคร...' : 'สมัคร'}
        </button>
      </div>
      <div className="right-tab"></div>
    </div>
  );
}

export default SignUpPass;