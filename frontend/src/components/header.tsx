import React from "react";
import "../styles/header.css";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <img
          src="src/assets/KU_logo.png"
          alt="Logo"
          className="logo"
        />
      </div>
      <div className="header-line"></div>
    </header>
  );
};

export default Header;
