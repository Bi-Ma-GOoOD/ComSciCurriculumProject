import React from "react";
import "../styles/header.css";

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="logo-container">
        <div className="logo"></div>
      </div>
      <div className="header-line"></div>
    </header>
  );
};

export default Header;
