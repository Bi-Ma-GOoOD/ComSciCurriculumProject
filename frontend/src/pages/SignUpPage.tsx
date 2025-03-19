// import React from 'react';
// import './SignUpPage.css';
// import { useNavigate } from 'react-router-dom';

// function SignUpPage() {
//   const navigate = useNavigate();
  
//     const handleNext = () => {
//       navigate('/OtpPage');
//     };
//   return (
//     <div className='container'>
//       <div className="left-tab"></div>

//       <div className='content'>
//         <div className="ku-logo"></div>
//         <div className="bottom-tab"></div>
//         <div className='title'>KU ComSci Graduate’s Check</div>
//       </div>

//       <div className='signup-page'>
//         <div className='title2'>ลงทะเบียนตรวจสอบหน่วยกิตและเช็คจบ</div>
//         <div className='email-title-signup'>Email (@ku)</div>
        
//         <div className='input-container'>
//           <input type="email" id="email" placeholder="abc@ku.th" className="email-input" />
//           <div className="checkbox-container">
//             <input type="checkbox" id="agree" />
//           </div>
//         </div>

//         <button className='next-signup-button' onClick={handleNext}>ถัดไป</button>
//       </div>

//       <div className="right-tab"></div>
//     </div>
//   );
// }

// export default SignUpPage;

import React, { useState } from 'react';
import '../styles/SignUpPage.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SignUpPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');

  const handleNext = async () => {
    // Validate email and agreement
    if (!email.trim()) {
      setError('Please enter an email');
      return;
    }

    // try {
    //   const response = await axios.post('http://localhost:8000/api/signup/', {
    //     email: email.trim()
    //   });

    //   if (response.data.success) {
    //     // Store reference for OTP verification
    //     localStorage.setItem('signupReference', response.data.reference);
    //     navigate('/OtpPage');
    //   }
    // } catch (err) {
    //   if (axios.isAxiosError(err)) {
    //     setError(err.response?.data?.message || 'Signup failed');
    //   } else {
    //     setError('Signup failed');
    //   }
    // }
    try {
      const response = await axios.post('http://localhost:8000/api/signup/', { email: email.trim() });
      console.log(response.data); // เช็ค response ที่ได้รับจาก backend
      if (response.data.success) {
        localStorage.setItem('signupReference', response.data.reference);
        localStorage.setItem('signupEmail', email.trim());
        // navigate('/OtpPage');
        navigate('/OtpPage', { state: { email: email.trim() } });
      } else {
        setError(response.data.message || 'Signup failed');
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.message || 'Signup failed');
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

        {error && <div className="error-message">{error}</div>}

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