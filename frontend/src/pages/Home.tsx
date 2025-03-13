import React from "react";
import { useNavigate } from "react-router-dom";
import Button from "../components/button";
import Header from "../components/header";
import "../styles/home.css";

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/creditcheck");
  };

  const handleClickGradutaionFile = () => {
    navigate("/insertgradfile");
  };

  return (
    <div className="home-page">
      <Header />
      <div className="content">
        <h1>Home Page</h1>
        <p>This is the home page. มันไม่มีอยู่จริงในโปรเจค</p>
        <div className="button-container">
          <Button
            text="To Credit Check"
            className="button"
            onClick={handleClick}
          />
          <Button
            text="To Insert Graduation File"
            className="button"
            onClick={handleClickGradutaionFile}
          />
        </div>
      </div>
    </div>
  );
};

export default HomePage;
