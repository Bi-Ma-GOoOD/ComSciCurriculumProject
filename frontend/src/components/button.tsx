import React from "react";
import "../styles/button.css";

interface ButtonProps {
  className: string;
  text: string;
  onClick?: () => void;
}

const Button: React.FC<ButtonProps> = ({
  className, text, onClick,}) => {
  return (
    <button
      className={`button ${className}`}
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default Button;
