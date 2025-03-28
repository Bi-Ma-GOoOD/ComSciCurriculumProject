import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/header";
import Button from "../components/button";
import UploadFileButton from "../components/uploadfile-button";
import ErrorMessage from "../components/ErrorMessage";
import SuccessMessage from "../components/SuccessMessage";
import ConfirmPopup from "../components/ConfirmPopup";
import "../styles/insertGradFile.css";
import axios from "axios";

const InsertGradFile: React.FC = () => {
  const [transcriptFile, setTranscriptFile] = useState<File | null>(null);
  const [activityFile, setActivityFile] = useState<File | null>(null);
  const [receiptFile, setReceiptFile] = useState<File | null>(null);
  const [selectedPage, setSelectedPage] = useState("insertgradfile");
  const [message, setMessage] = useState<string | null>(null);
  const [messageType, setMessageType] = useState<"error" | "success" | null>(
    null
  );
  const [showCalculateButton, setCalculateButton] = useState(false);
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [navigateTo, setNavigateTo] = useState<string | null>(null);
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    setFile: React.Dispatch<React.SetStateAction<File | null>>
  ) => {
    const selectedFile = event.target.files?.[0];
    setFile(selectedFile || null);
  };

  const handleRemoveFile = (
    setFile: React.Dispatch<React.SetStateAction<File | null>>
  ) => {
    setFile(null);
  };

  const handleSubmit = async () => {
    if (!transcriptFile || !activityFile || !receiptFile) {
      setMessage("กรุณาแนบไฟล์ให้ครบทั้ง 3 ไฟล์");
      setMessageType("error");
    } else if (
      (transcriptFile && transcriptFile.type !== "application/pdf") ||
      (activityFile && activityFile.type !== "application/pdf") ||
      (receiptFile && receiptFile.type !== "application/pdf")
    ) {
      setMessage("ไฟล์แนบต้องเป็น PDF");
      setMessageType("error");
    } else {
      const formData = new FormData();
      formData.append("transcript", transcriptFile);
      formData.append("activity", activityFile);
      formData.append("receipt", receiptFile);
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
      navigate("/verify-result")
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
    if (transcriptFile || activityFile || receiptFile) {
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
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className="grad-file-container">
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
            <span className="upload-text"> แนบไฟล์ผลการเรียน*</span>
            <UploadFileButton
              onChange={(e) => handleFileChange(e, setTranscriptFile)}
              onRemoveFile={() => handleRemoveFile(setTranscriptFile)}
            />
          </div>
          <p />
          <div className="upload-section">
            <span className="upload-text">แนบไฟล์กิจกรรม*</span>
            <UploadFileButton
              onChange={(e) => handleFileChange(e, setActivityFile)}
              onRemoveFile={() => handleRemoveFile(setActivityFile)}
            />
          </div>
          <p />
          <div className="upload-section">
            <span className="upload-text">แนบหลักฐานการชำระค่าเทอม*</span>
            <UploadFileButton
              onChange={(e) => handleFileChange(e, setReceiptFile)}
              onRemoveFile={() => handleRemoveFile(setReceiptFile)}
            />
          </div>
          {message && (
            <div className="message-container">
              {messageType === "success" ? (
                <SuccessMessage message={message} />
              ) : (
                <ErrorMessage message={message} />
              )}
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
        <ConfirmPopup
          message="หากเปลี่ยนเป็นฟอร์ม ไฟล์ที่แนบไว้จะหายไป คุณต้องการดำเนินการต่อหรือไม่?"
          onConfirm={confirmNavigation}
          onCancel={cancelNavigation}
        />
      )}
      <div className="right-tab"></div>
    </div>
  );
};

export default InsertGradFile;