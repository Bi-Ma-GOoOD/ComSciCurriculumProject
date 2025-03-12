import React from "react";
import "../styles/header.css";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <img
          src="./KU_Logo_JPG.jpg"
          alt="Logo"
          className="logo"
        />
      </div>
      <div className="header-line"></div>
    </header>
  );
};

export default Header;
