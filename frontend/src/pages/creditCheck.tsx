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
  const [showCalculateButton, setCalculateButton] = useState(false);
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [navigateTo, setNavigateTo] = useState<string | null>(null);
  const [selectedPage, setSelectedPage] = useState("creditcheck");
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");

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
      formData.append("user_id", user?.id ?? ''); // Include user_id in the request

      try {
        const response = await axios.post(
          "http://localhost:8000/api/upload/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        setMessage("ไฟล์ถูกต้อง");
        setMessageType("success");
        setCalculateButton(true);
        console.log("Files sent to backend:", response.data);
      } catch (error) {
        setMessage("เกิดข้อผิดพลาดในการอัปโหลดไฟล์");
        setMessageType("error");
        console.error("Error uploading files:", error);
      }
    }
  };

  const handleCalculationSubmit = async () => {
    const response = await axios.post(`http://localhost:8000/api/calculate/?uid=${user?.id}`);
    console.log(response.data)
    if (response.data.success) {
      navigate("/verify-result");
    }
  }
  
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage(null);
        setMessageType(null);
      }, 1500); // 3 seconds

      return () => clearTimeout(timer);
    }
  }, [message]);

  const handleNavigate = async (page: string) => {
    if (file) {
      setShowConfirmPopup(true);
      setNavigateTo(page);
    } else {
      setSelectedPage(page);
      const response = await axios.put(
        `http://localhost:8000/api/upload/?uid=${user?.id}&form_type=${page}`,
      );
      console.log(response.data)
      navigate(`/${page}`);
    }
  };

  const confirmNavigation = async () => {
    if (navigateTo) {
      setSelectedPage(navigateTo);
      const response = await axios.put(
        `http://localhost:8000/api/upload/?uid=${user?.id}&form_type=${navigateTo}`,
      );
      console.log(response.data)
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
      <div className="left-tab"></div>
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
            <UploadFileButton
              onChange={handleFileChange}
              onRemoveFile={handleRemoveFile}
            />
          </div>
          <p />
          <div className="upload-section faded">
            <span className="upload-text">แนบไฟล์กิจกรรม*</span>
            <UploadFileButton
              onChange={handleFileChange}
              onRemoveFile={handleRemoveFile}
            />
          </div>
          <p />
          <div className="upload-section faded">
            <span className="upload-text">แนบหลักฐานการชำระค่าเทอม*</span>
            <UploadFileButton
              onChange={handleFileChange}
              onRemoveFile={handleRemoveFile}
            />
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
          {showCalculateButton && (
            <Button
              text="ส่ง"
              className="button calculate-button"
              onClick={handleCalculationSubmit}
            />
          )}
          {!showCalculateButton && (
            <Button
            text="ตรวจสอบไฟล์"
            className="button"
            onClick={handleSubmit}
          />
          )}
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
      <div className="right-tab"></div>
    </div>
  );
};

export default CreditCheckPage;
