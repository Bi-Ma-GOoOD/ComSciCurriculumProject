import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from "../components/header";
import "../styles/fileAttachCheck.css";
import Swal from 'sweetalert2';

interface FormData {
  student_code: string;
  form_status: string;
  form_id: string;
}

const FileAttachCheck: React.FC = () => {
  const [formData, setFormData] = useState<FormData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFormData = async () => {
      // Retrieve user from localStorage
      const user = localStorage.getItem('user');
      
      if (!user) {
        Swal.fire({
          title: "กรุณาเข้าสู่ระบบ",
          text: "คุณต้องเข้าสู่ระบบก่อนเข้าใช้งาน",
          icon: "warning",
          confirmButtonText: "OK",
          confirmButtonColor: "#B2BB1E"
        }).then(() => {
          navigate('/');
        });
        return;
      }
  
      try {
        setIsLoading(true);
        const response = await axios.get('http://localhost:8000/api/pending-forms/', {
          headers: {
            'Content-Type': 'application/json',
          }
        });
  
        if (response.data.forms) {
          setFormData(response.data.forms);
        } else {
          setFormData([]);
        }
      } catch (error: any) {
        console.error('Error fetching form data:', error);
        
        if (error.response?.status === 401) {
          Swal.fire({
            title: "หมดเวลาเข้าสู่ระบบ",
            text: "กรุณาเข้าสู่ระบบอีกครั้ง",
            icon: "warning",
            confirmButtonText: "OK",
            confirmButtonColor: "#B2BB1E"
          }).then(() => {
            localStorage.clear();
            navigate('/');
          });
        } else {
          Swal.fire({
            title: "เกิดข้อผิดพลาด",
            text: "ไม่สามารถดึงข้อมูลได้ กรุณาลองใหม่",
            icon: "error",
            confirmButtonText: "OK",
            confirmButtonColor: "#B2BB1E"
          });
        }
      } finally {
        setIsLoading(false);
      }
    };
  
    fetchFormData();
  }, [navigate]);

  const handleFileClick = (user: FormData) => {
    navigate('/fileAttachList', { state: { user } });
  };

  return (
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className='page-name'>ตรวจสอบไฟล์แนบจบนิสิต</div>
        <div className="file-check-container">
          <div className="list-container">
            <table className="file-list">
              <thead>
                <tr>
                  <th>รหัสนิสิต</th>
                  <th>สถานะการตรวจสอบ</th>
                  <th>ไฟล์</th>
                </tr>
              </thead>
              <tbody>
                {isLoading ? (
                  <tr>
                    <td colSpan={3}>กำลังโหลดข้อมูล...</td>
                  </tr>
                ) : formData.length === 0 ? (
                  <tr>
                    <td colSpan={3}>ไม่มีข้อมูล</td>
                  </tr>
                ) : (
                  formData.map((form, index) => (
                    <tr key={index}>
                      <td className="id-column">{form.student_code}</td>
                      <td className="check-column">{form.form_status}</td>
                      <td 
                        className="file-column cursor-pointer hover:text-blue-600 button-style"
                        onClick={() => handleFileClick(form)}
                      >
                        ไฟล์
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
};

export default FileAttachCheck;