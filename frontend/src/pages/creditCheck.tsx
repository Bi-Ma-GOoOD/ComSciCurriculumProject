import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/header";
import Button from "../components/button";
import UploadFileButton from "../components/uploadfile-button";
import "../styles/creditCheck.css";
import { IoWarningOutline } from "react-icons/io5";
import axios from "axios";

const CreditCheckPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<"error" | "success" | null>(
    null
  );
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [navigateTo, setNavigateTo] = useState<string | null>(null);
  const [selectedPage, setSelectedPage] = useState("creditcheck");
  const navigate = useNavigate();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    setFile(selectedFile || null);
  };

  const handleRemoveFile = () => {
    setFile(null);
  };

  const handleSubmit = async () => {
    if (!file) {
      setMessage("ไม่สามารถตรวจสอบไฟล์ได้");
      setMessageType("error");
      return;
    }
    if (file && file.type !== "application/pdf") {
      setMessage("ไฟล์แนบต้องเป็น PDF");
      setMessageType("error");
    } else {
      const formData = new FormData();
      formData.append("transcript", file);

      try {
        const response = await axios.post("http://localhost:8000/api/upload/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        setMessage("ไฟล์ถูกต้อง");
        setMessageType("success");
        console.log("Files sent to backend:", response.data);
      } catch (error) {
        setMessage("เกิดข้อผิดพลาดในการอัปโหลดไฟล์");
        setMessageType("error");
        console.error("Error uploading files:", error);
      }
    }
  };

  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage(null);
        setMessageType(null);
      }, 3000); // 3 seconds

      return () => clearTimeout(timer);
    }
  }, [message]);

  const handleNavigate = (page: string) => {
    if (file) {
      setShowConfirmPopup(true);
      setNavigateTo(page);
    } else {
      setSelectedPage(page);
      navigate(`/${page}`);
    }
  };

  const confirmNavigation = () => {
    if (navigateTo) {
      setSelectedPage(navigateTo);
      navigate(`/${navigateTo}`);
    }
    setShowConfirmPopup(false);
  };

  const cancelNavigation = () => {
    setShowConfirmPopup(false);
    setNavigateTo(null);
  };

  return (
    <div className="credit-check-page">
      <Header />
      <div className="content">
        <div className="credit-check-container">
          <div className="button-container">
            <label>
              <input
                type="radio"
                name="page"
                value="insertgradfile"
                checked={selectedPage === "insertgradfile"}
                onChange={() => handleNavigate("insertgradfile")}
              />
              ต้องการเช็คจบ
            </label>
            <label>
              <input
                type="radio"
                name="page"
                value="creditcheck"
                checked={selectedPage === "creditcheck"}
                onChange={() => handleNavigate("creditcheck")}
              />
              ต้องการเช็คหน่วยกิต
            </label>
          </div>
          <div className="upload-section">
            <span className="upload-text">แนบไฟล์ผลการเรียน*</span>
            <UploadFileButton onChange={handleFileChange} onRemoveFile={handleRemoveFile} />
          </div>
          <p />
          <div className="upload-section faded">
            <span className="upload-text">
              แนบไฟล์กิจกรรม*
            </span>
            <UploadFileButton onChange={handleFileChange} onRemoveFile={handleRemoveFile} />
          </div>
          <p />
          <div className="upload-section faded">
            <span className="upload-text">แนบหลักฐานการชำระค่าเทอม*</span>
            <UploadFileButton onChange={handleFileChange} onRemoveFile={handleRemoveFile} />
          </div>
          {message && (
            <div className="message-container">
              <p
                className={
                  messageType === "success"
                    ? "success-message"
                    : "error-message"
                }
              >
                {message}
              </p>
            </div>
          )}
          <p />
          <Button text="ตรวจสอบไฟล์" className="button" onClick={handleSubmit} />
        </div>
      </div>
      {showConfirmPopup && (
        <div className="confirm-popup">
          <IoWarningOutline className="warning-icon" />
          <p>
            หากเปลี่ยนเป็นฟอร์ม ไฟล์ที่แนบไว้จะหายไป
            คุณต้องการดำเนินการต่อหรือไม่?
          </p>
          <Button
            text="ยืนยัน"
            className="confirm-button"
            onClick={confirmNavigation}
          />
          <Button
            text="ยกเลิก"
            className="cancel-button"
            onClick={cancelNavigation}
          />
        </div>
      )}
    </div>
  );
};

export default CreditCheckPage;
