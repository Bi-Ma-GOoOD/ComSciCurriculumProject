// import React, { useState } from 'react';
// import './SignUpPass.css';

// function SignUpPass() {
//   const [role, setRole] = useState("Roles");
//   const [isOpen, setIsOpen] = useState(false);
//   const roles = ["นิสิต", "ผู้ตรวจสอบหลักฐาน"];
  
//   // กำหนด placeholder ตาม role ที่เลือก
//   const getPlaceholder = () => {
//     if (role === "นิสิต") {
//       return "รหัสนิสิต";
//     } else if (role === "ผู้ตรวจสอบหลักฐาน") {
//       return "key";
//     }
//     return "";
//   };

//   return (
//     <div className='container'>
//       <div className="left-tab"></div>
//       <div className='content'>
//         <div className="ku-logo"></div>
//         <div className="bottom-tab"></div>
//         <div className='title'>KU ComSci Graduate’s Check</div>
//       </div>
//       <div className='signup-password'>
//         <div className='title2'>ลงทะเบียนตรวจสอบหน่วยกิตและเช็คจบ</div>
//         <div className='password-title'>Password</div>
//         <input type="password" id="password" placeholder="1234abcd" className="password-input" />
//         <div className='confirm-password-title'>Confirm Password</div>
//         <input type="password" id="confirm-password" placeholder="1234abcd" className="confirm-password-input" />
        
//         <div className="input-group">
//           <div className="dropdown-container">
//             <button className="dropdown-button" onClick={() => setIsOpen(!isOpen)}>
//               <span>{role}</span>
//               <span className="dropdown-icon">▼</span>
//             </button>
//             {isOpen && (
//               <ul className="dropdown-menu">
//                 {roles.map((option) => (
//                   <li key={option} onClick={() => { setRole(option); setIsOpen(false); }}>
//                     {option}
//                   </li>
//                 ))}
//               </ul>
//             )}
//           </div>
          
//           <input type="text" className="id-student-input" placeholder={getPlaceholder()} />
//         </div>

//         <button className='register-button'>สมัคร</button>
//       </div>
//       <div className="right-tab"></div>
//     </div>
//   );
// }

// export default SignUpPass;

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import '../styles/SignUpPass.css';

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
    name: ''  // You can add name field if needed
  });
  
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState('');
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
      setError("Email information missing. Please restart the signup process.");
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
  const handleChange = (e) => {
    const { id, value } = e.target;
    setFormData(prev => ({ ...prev, [id]: value }));
  };
  
  // Handle role selection
  const handleRoleSelect = (role) => {
    setFormData(prev => ({ ...prev, role, studentCode: '', keyCode: '' }));
    setIsOpen(false);
  };
  
  // Handle code/key input based on role
  const handleCodeChange = (e) => {
    const value = e.target.value;
    if (formData.role === "นิสิต") {
      setFormData(prev => ({ ...prev, studentCode: value }));
    } else if (formData.role === "ผู้ตรวจสอบหลักฐาน") {
      setFormData(prev => ({ ...prev, keyCode: value }));
    }
  };
  
  // Submit registration
  const handleRegister = async () => {
    // Reset error
    setError('');
    
    // Validate form
    if (!formData.email) {
      setError('Email is required');
      return;
    }
    
    if (!formData.password) {
      setError('Password is required');
      return;
    }
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    
    if (formData.role === 'Roles') {
      setError('Please select a role');
      return;
    }
    
    if (formData.role === "นิสิต" && !formData.studentCode) {
      setError('Student code is required');
      return;
    }
    
    if (formData.role === "ผู้ตรวจสอบหลักฐาน" && !formData.keyCode) {
      setError('Key code is required');
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
        
        // Show success message
        alert('Registration successful!');
        
        // Redirect to login page
        navigate('/');
      }
    } catch (err) {
      console.error('Registration error:', err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Registration failed');
      } else {
        setError('Registration failed');
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
        
        {error && <div className="error-message">{error}</div>}
        
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