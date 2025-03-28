import React from "react";
import Button from "./button";
import { IoWarningOutline } from "react-icons/io5";
import "../styles/ConfirmPopup.css";

interface ConfirmPopupProps {
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const ConfirmPopup: React.FC<ConfirmPopupProps> = ({ message, onConfirm, onCancel }) => {
  return (
    <div className="confirm-popup">
      <IoWarningOutline className="warning-icon" />
      <p>{message}</p>
      <Button text="ยืนยัน" className="confirm-button" onClick={onConfirm} />
      <Button text="ยกเลิก" className="cancel-button" onClick={onCancel} />
    </div>
  );
};

export default ConfirmPopup;
