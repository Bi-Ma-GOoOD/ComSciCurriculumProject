// import React from "react";
// import Header from "../components/header";
// import Button from "../components/button";
// import "../styles/fileAttachList.css";

// const FileAttachList: React.FC = () => {
//   const handleInspectFile = (fileName: string) => {
//     // Logic to inspect the PDF file
//     console.log('Inspecting: ${fileName}');
//   };

//   return (
//     <div className="grad-file-page">
//       <Header />
//       <div className="left-tab"></div>
//       <div className="content">
//         <div className='page-name'>6510450208</div>
//         <div className="grad-file-container">
//           <div className='inspect-file-container'>
//             <div className='student-code'>6510450208</div>
//             <Button
//               text="my_transcript.pdf"
//               className="inspect-button"
//               onClick={() => handleInspectFile("my_transcript.pdf")}
//             />
//             <div className="download-file-text">ดาวน์โหลดใบผลการเรียน</div>
//             <Button
//               text="my_activity.pdf"
//               className="inspect-button"
//               onClick={() => handleInspectFile("my_activity.pdf")}
//             />
//             <div className="download-file-text">ดาวน์โหลดใบผลการร่วมกิจกรรม</div>
//             <Button
//               text="my_receipt.pdf"
//               className="inspect-button"
//               onClick={() => handleInspectFile("my_receipt.pdf")}
//             />
//             <div className="download-file-text">ดาวน์โหลดใบเสร็จการชำระค่าธรรมเนียม</div>

//             <div className="download-check-text">ดาวน์โหลดใบตรวจสอบหลักสูตร</div>

//             <Button
//               text="ตรวจสอบไฟล์"
//               className="button"
//               //onClick={handleInspectFile} ขั้นตอนตรวจสอบไฟล์ เปลี่ยนสถานะ?
//             />
//           </div>
//         </div>
//       </div>
//       <div className="right-tab"></div>
//     </div>
//   );
// };

// export default FileAttachList;


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

  const handleDownloadFile = async (fileType: string) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/file-attach-list/`, {
        params: { 
          form_id: formId, 
          file_type: fileType,
          download: 'true'
        },
        responseType: 'blob'
      });

      // Create a link element to trigger download
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${studentCode}_${fileType}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error downloading file:', error);
      Swal.fire({
        title: "เกิดข้อผิดพลาด",
        text: "ไม่สามารถดาวน์โหลดไฟล์ได้",
        icon: "error",
        confirmButtonText: "OK"
      });
    }
  };

  const handleVerifyFiles = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/file-attach-list/', {
        form_id: formId
      });

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
            <div className='student-code'>{studentCode}</div>
            
            {/* Transcript */}
            <Button
              text="ใบผลการเรียน"
              className="inspect-button"
              onClick={() => handleInspectFile(fileUrls.transcript)}
            />
            <div className="download-file-text">
              <Button
                text="ดาวน์โหลด"
                className="download-button"
                onClick={() => handleDownloadFile('transcript')}
              />
            </div>
            
            {/* Activity Certificate */}
            <Button
              text="ใบผลการร่วมกิจกรรม"
              className="inspect-button"
              onClick={() => handleInspectFile(fileUrls.activity)}
            />
            <div className="download-file-text">
              <Button
                text="ดาวน์โหลด"
                className="download-button"
                onClick={() => handleDownloadFile('activity')}
              />
            </div>
            
            {/* Receipt */}
            <Button
              text="ใบเสร็จการชำระค่าธรรมเนียม"
              className="inspect-button"
              onClick={() => handleInspectFile(fileUrls.receipt)}
            />
            <div className="download-file-text">
              <Button
                text="ดาวน์โหลด"
                className="download-button"
                onClick={() => handleDownloadFile('receipt')}
              />
            </div>

            <Button
              text="ตรวจสอบไฟล์"
              className="button"
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