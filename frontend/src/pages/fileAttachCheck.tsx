import React from "react";
import Header from "../components/header";
import "../styles/fileAttachCheck.css";

const FileAttachCheck: React.FC = () => {
  return (
    <div className="grad-file-page">
      <Header />
      <div className="left-tab"></div>
      <div className="content">
        <div className='page-name'>ตรวจสอบไฟล์แนบจบนิสิต</div>
        <div className="grad-file-container">
          <p />
          {/* Add your content here */}
          <div className="list-container">
            <table className="file-list">
              <tbody>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ตรวจสอบแล้ว</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">6510450208</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ตรวจสอบแล้ว</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ตรวจสอบแล้ว</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                <tr>
                  <td className="id-column">64xxxxxxxx</td>
                  <td className="check-column">ยังไม่ได้ตรวจสอบ</td>
                  <td className="file-column">ไฟล์</td>
                </tr>
                {/* Add more rows as needed */}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div className="right-tab"></div>
    </div>
  );
};

export default FileAttachCheck;
