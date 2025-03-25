import React from "react";
import Header from "../components/header";
import Button from "../components/button";
import "../styles/fileAttachList.css";

const FileAttachList: React.FC = () => {
  const handleInspectFile = (fileName: string) => {
    // Logic to inspect the PDF file
    console.log('Inspecting: ${fileName}');
  };

  return (
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className='page-name'>6510450208</div>
        <div className="grad-file-container">
          <div className='inspect-file-container'>
            <div className='student-code'>6510450208</div>
            <Button
              text="my_transcript.pdf"
              className="inspect-button"
              onClick={() => handleInspectFile("my_transcript.pdf")}
            />
            <div className="download-file-text">ดาวน์โหลดใบผลการเรียน</div>
            <Button
              text="my_activity.pdf"
              className="inspect-button"
              onClick={() => handleInspectFile("my_activity.pdf")}
            />
            <div className="download-file-text">ดาวน์โหลดใบผลการร่วมกิจกรรม</div>
            <Button
              text="my_receipt.pdf"
              className="inspect-button"
              onClick={() => handleInspectFile("my_receipt.pdf")}
            />
            <div className="download-file-text">ดาวน์โหลดใบเสร็จการชำระค่าธรรมเนียม</div>

            <div className="download-check-text">ดาวน์โหลดใบตรวจสอบหลักสูตร</div>

            <Button
              text="ตรวจสอบไฟล์"
              className="button"
              //onClick={handleInspectFile} ขั้นตอนตรวจสอบไฟล์ เปลี่ยนสถานะ?
            />
          </div>
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
};

export default FileAttachList;
