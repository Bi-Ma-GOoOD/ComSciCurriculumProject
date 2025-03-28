import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Header from "../components/header";
import Button from "../components/button";
import Swal from 'sweetalert2';
import "../styles/fileAttachList.css";

interface FileUrls {
  transcript?: string;
  activity?: string;
  receipt?: string;
}

const FileAttachList: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [studentCode, setStudentCode] = useState<string>('');
  const [fileUrls, setFileUrls] = useState<FileUrls>({});
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [formId, setFormId] = useState<string>('');

  useEffect(() => {
    const fetchFileDetails = async () => {
      const user = location.state?.user;
      
      if (!user) {
        Swal.fire({
          title: "ข้อผิดพลาด",
          text: "ไม่พบข้อมูลฟอร์ม",
          icon: "error",
          confirmButtonText: "OK"
        });
        navigate('/fileAttachCheck');
        return;
      }

      try {
        const response = await axios.get(`http://localhost:8000/api/file-attach-list/`, {
          params: { form_id: user.form_id }
        });

        setStudentCode(response.data.form_details.student_code);
        setFileUrls(response.data.file_urls);
        setFormId(user.form_id);
      } catch (error) {
        console.error('Error fetching file details:', error);
        Swal.fire({
          title: "เกิดข้อผิดพลาด",
          text: "ไม่สามารถดึงข้อมูลไฟล์ได้",
          icon: "error",
          confirmButtonText: "OK"
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchFileDetails();
  }, [location, navigate]);

  const handleInspectFile = (fileUrl: string | undefined) => {
    if (fileUrl) {
      window.open(fileUrl, '_blank');
    } else {
      Swal.fire({
        title: "ไม่พบไฟล์",
        text: "ไม่สามารถเปิดไฟล์ได้",
        icon: "warning",
        confirmButtonText: "OK"
      });
    }
  };

  const handleVerifyFiles = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/file-attach-list/', {
        form_id: formId
      });
      console.log('File verification response:', response.data);

      Swal.fire({
        title: "ตรวจสอบสำเร็จ",
        text: "ดำเนินการตรวจสอบไฟล์เรียบร้อย",
        icon: "success",
        confirmButtonText: "OK"
      }).then(() => {
        navigate('/fileAttachCheck');
      });
    } catch (error) {
      Swal.fire({
        title: "เกิดข้อผิดพลาด",
        text: "ไม่สามารถตรวจสอบไฟล์ได้",
        icon: "error",
        confirmButtonText: "OK"
      });
    }
  };

  if (isLoading) {
    return <div>กำลังโหลดข้อมูล...</div>;
  }

  return (
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className='page-name'>{studentCode}</div>
        <div className="grad-file-container">
          <div className='inspect-file-container'>
            {/* Transcript */}
            <Button
              text="ใบผลการเรียน"
              className="inspect-button button-style"
              onClick={() => handleInspectFile(fileUrls.transcript)}
            />
            {/* Activity Certificate */}
            <Button
              text="ใบผลการร่วมกิจกรรม"
              className="inspect-button"
              onClick={() => handleInspectFile(fileUrls.activity)}
            />
            {/* Receipt */}
            <Button
              text="ใบเสร็จการชำระค่าธรรมเนียม"
              className="inspect-button"
              onClick={() => handleInspectFile(fileUrls.receipt)}
            />
            <Button
              text="ตรวจสอบไฟล์"
              className="button button-style"
              onClick={handleVerifyFiles}
            />
          </div>
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
};

export default FileAttachList;