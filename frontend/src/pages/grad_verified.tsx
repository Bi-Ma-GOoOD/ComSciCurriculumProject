import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import '../styles/GradVerifiedPage.css';
import { faCircleArrowLeft, faCircleCheck, faCircleXmark, faCircle } from '@fortawesome/free-solid-svg-icons';
import { useState } from 'react';


function GradVerifiedPage() {
const [isPass, setIsPass] = useState(false);

  return (
    <div className='container'>
      <div className="left-tab"></div>

      <div className='content'>
        <div className="ku-logo"></div>
        <div className="bottom-tab"></div>
        <FontAwesomeIcon 
          icon={faCircleArrowLeft} 
          className="back-arrow"
          onClick={() => window.history.back()}
        />
         <div className={`verification-status ${isPass ? 'pass' : 'fail'}`}>
            <FontAwesomeIcon 
                icon={isPass ? faCircleCheck : faCircleXmark}
                className="status-icon"
            />
            <div className="status-text-container">
                <span className="verified-text">Verified</span>
                <span className="status-result">{isPass ? 'ผ่าน' : 'ไม่ผ่าน'}</span>
            </div>
            </div>
            <div className='content'>
            <div className="credits-container">
  <div className="credits-section">
    {/* หมวดวิชาศึกษาทั่วไป */}
    <div className="section-item">
      <div className="sub-item">
        <FontAwesomeIcon 
          icon={faCircle} 
          className={`status-circle ${isPass ? 'pass' : 'fail'}`}
        />
        <h2>หมวดวิชาศึกษาทั่วไป (25/30)</h2>
      </div>
      <div className="sub-items">
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>กลุ่มสาระอยู่ดีมีสุข (3/3)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>กลุ่มสาระศาสตร์แห่งผู้ประกอบการ (3/3)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle fail"
          />
          <span>กลุ่มสาระภาษากับการสื่อสาร (10/13)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>กลุ่มสาระพลเมืองไทยและพลเมืองโลก (3/3)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>กลุ่มสาระสุนทรียศาสตร์ (3/3)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle fail"
          />
          <span>เลือกเรียนรายวิชาใน 5 กลุ่มสาระ (3/5)</span>
        </div>
      </div>
    </div>

    {/* หมวดวิชาเฉพาะ */}
    <div className="section-item">
      <div className="sub-item">
        <FontAwesomeIcon 
          icon={faCircle} 
          className={`status-circle ${isPass ? 'pass' : 'fail'}`}
        />
        <h2>หมวดวิชาเฉพาะ (79/88)</h2>
      </div>
      <div className="sub-items">
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>วิชาแกน (12/12)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle fail"
          />
          <span>วิชาเฉพาะบังคับ (49/58)</span>
        </div>
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>วิชาเฉพาะเลือก (18/18)</span>
        </div>
      </div>
    </div>

    {/* หมวดวิชาเลือกเสรี */}
    <div className="section-item">
      <div className="sub-item">
        <FontAwesomeIcon 
          icon={faCircle} 
          className={`status-circle pass`}
        />
        <h2>หมวดวิชาเลือกเสรี (9/6)</h2>
      </div>
      <div className="sub-items">
        <div className="sub-item">
          <FontAwesomeIcon 
            icon={faCircle} 
            className="status-circle pass"
          />
          <span>หมวดวิชาเลือกเสรี (9/6)</span>
        </div>
      </div>
    </div>
  </div>
</div>
<div className="activity-credits">
  <span>จำนวนกิจกรรม (113/124)</span>
  <FontAwesomeIcon 
    icon={faCircle} 
    className={`status-circle ${isPass ? 'pass' : 'fail'}`}
  />
  <span>จำนวนชั่วโมง 30</span>
  <FontAwesomeIcon 
    icon={faCircle} 
    className={`status-circle ${isPass ? 'pass' : 'fail'}`}
  />
</div>
            </div>
      </div>

      <div className="right-tab"></div>
    </div>
  );
}

export default GradVerifiedPage;