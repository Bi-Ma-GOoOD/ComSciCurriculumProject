import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import Swal from 'sweetalert2';
import '../styles/OtpPage.css';

function OtpPage() {
  const [otp, setOtp] = useState(new Array(6).fill(""));
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // Get email from localStorage or location state
  useEffect(() => {
    const storedEmail = localStorage.getItem('signupEmail');
    
    if (storedEmail) {
      setEmail(storedEmail);
    } else if (location.state?.email) {
      setEmail(location.state.email);
      localStorage.setItem('signupEmail', location.state.email);
    } else {
      setError("Email information missing. Please go back to the signup page.");
    }
  }, [location]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>, index: number) => {
    const value = e.target.value.replace(/\D/g, ""); // Only accept numbers
    if (value.length > 1) return; // Limit to one digit per field

    const newOtp = [...otp];
    newOtp[index] = value;
    setOtp(newOtp);

    // Move focus to next input
    if (value && index < 5) {
      const nextInput = document.getElementById(`input${index + 2}`);
      if (nextInput) nextInput.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      const prevInput = document.getElementById(`input${index}`);
      if (prevInput) prevInput.focus();
    }
  };

  const handleNext = async () => {
    // Clear previous errors
    setError("");
    
    // Check if all OTP fields are filled
    const otpString = otp.join("");
    if (otpString.length !== 6) {
      Swal.fire({
        title: "ไม่สามารถลงทะเบียนได้",
        text: "กรุณากรอก OTP ให้ครบ 6 หลัก",
        icon: "warning",
        confirmButtonText: "OK",
        confirmButtonColor: "#B2BB1E"
      });
      return;
    }
    console.log("OTP being submitted:", otpString, typeof otpString);
    if (otpString.length !== 6) {
      setError("Please enter all 6 digits of the OTP");
      return;
    }

    // Check if email is available
    if (!email) {
      setError("Email information missing. Please go back to signup page.");
      return;
    }

    setIsSubmitting(true);
    
    try {
      const response = await axios.post('http://localhost:8000/api/verify-otp/', {
        email: email,
        otp: otpString.toString()
      });

      if (response.data.success) {
        Swal.fire({
          title: "OTP ยืนยันสำเร็จ",
          icon: "success",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        }).then(() => {
          localStorage.setItem('signupEmail', email);
          navigate('/SignUpPass', { 
            state: { email: email }
          });
        });
      } else {
        Swal.fire({
          title: "OTP ไม่ถูกต้อง",
          text: "กรุณากรอก OTP ให้ถูกต้อง",
          icon: "error",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        });
      }
      }catch (err) {
      console.error('OTP verification error:', err);
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'OTP verification failed');
      } else {
        setError('OTP verification failed');
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
      <div className='otp'>
        <div className='titleOtp'>OTP verification</div>
        {email && (
          <div className="email-display">
            Code sent to: {email}
          </div>
        )}
        <div className="otp-container">
          <div className='otp-input'>
            {otp.map((digit, index) => (
              <input
                key={index}
                id={`input${index + 1}`}
                type='text'
                maxLength={1}
                value={digit}
                onChange={(e) => handleChange(e, index)}
                onKeyDown={(e) => handleKeyDown(e, index)}
                disabled={isSubmitting}
              />
            ))}
          </div>
        </div>
        
        {error && <div className="error-message">{error}</div>}
        
        <button 
          className='next-otp-button' 
          onClick={handleNext}
          disabled={isSubmitting}
        >
          {isSubmitting ? 'Verifying...' : 'ถัดไป'}
        </button>
      </div>
      <div className="right-tab"></div>
    </div>
  );
}

export default OtpPage;