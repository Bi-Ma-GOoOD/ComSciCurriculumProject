import React from "react";
import Header from "../components/header";
import "../styles/fileAttachList.css";

const FileAttachList: React.FC = () => {
  return (
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className='page-name'>6510450208</div>
        <div className="grad-file-container">
          <div className='inspect-file-container'>
            
          </div>
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
};

export default FileAttachList;
