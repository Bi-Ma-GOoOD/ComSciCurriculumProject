import React from "react";
import "../styles/InsertGradFile.css";

interface SuccessMessageProps {
  message: string;
}

const SuccessMessage: React.FC<SuccessMessageProps> = ({ message }) => {
  return <p className="success-message">{message}</p>;
};

export default SuccessMessage;
