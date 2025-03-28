import React from "react";
import "../styles/InsertGradFile.css";

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return <p className="error-message">{message}</p>;
};

export default ErrorMessage;
