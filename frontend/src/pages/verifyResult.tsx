import { useEffect, useState } from "react";
import Header from "../components/header";
import axios from "axios";
import "../styles/verifyResult.css";
import Button from "../components/button";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";

const moreInfomationURL =
  "https://cs.sci.ku.ac.th/degree-info/undergraduate/curriculum";

// Define the interface for the result data
interface StudyResult {
  is_pass: boolean;
  total_min_credit: number;
  acquired_credit: number;
  result: CategoryResult[];
  not_pass_course: NotPassCourse[];
}

interface CategoryResult {
  category_name: string;
  is_pass: boolean;
  acquired_credit: number;
  total_min_credit: number;
  subcategories: {
    subcategory_name: string;
    acquired_credit: number;
    total_min_credit: number;
    is_pass: boolean;
  }[];
}

interface NotPassCourse {
  course_id: string;
  course_name_th: string;
  course_name_en: string;
  grade: string;
}

interface ResultData {
  form_status: string;
  fee_result: boolean;
  activity_result: boolean;
  study_result: StudyResult;
}

export default function VerifyResultPage() {
  const [graduateCheckResult, setGraduateCheckResult] =
    useState<ResultData | null>(null);
  const [nonGraduateCheckResult, setNonGraduateCheckResult] =
    useState<StudyResult | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    const fetchData = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/credit-verify/?uid=${user?.id}`
        );

        if (response.status === 200) {
          console.log(response.data);

          if (response.data.is_graduate_check) {
            setGraduateCheckResult(response.data.message);
          } else {
            setNonGraduateCheckResult(response.data.message);
          }
        }

        return response.data;
      } catch (error) {
        console.error("Error verifying credit:", error);
      }
    };

    fetchData();
  }, []);

  const handleResubmitFile = async () => {
    const result = await Swal.fire({
      title: "ต้องการแนบไฟล์ใหม่หรือไม่?",
      text: "ข้อมูลการตรวจสอบปัจจุบันของคุณจะถูกลบออกจากระบบ",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "ยืนยัน",
      cancelButtonText: "ยกเลิก",
      confirmButtonColor: "#FF0000",
      cancelButtonColor: "#DBDBDB",
      customClass: {
        confirmButton: "custom-confirm-button",
        cancelButton: "custom-cancel-button",
      },
    });

    if (result.isConfirmed) {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      const response = await axios.delete(
        `http://localhost:8000/api/credit-verify/?uid=${user?.id}`
      );
      if (response.status === 200) {
        console.log(response.data);
        navigate("/insertgradfile");
      }
    }
  };

  return (
    <div className="content">
      <Header />
      <div className="verify-result-content">
        {/* occure only when verification have not pass courses */}
        {graduateCheckResult &&
          graduateCheckResult.study_result.not_pass_course.length != 0 && (
            <VerifyResult
              status={
                graduateCheckResult.fee_result &&
                graduateCheckResult.activity_result &&
                graduateCheckResult.study_result.is_pass
              }
            />
          )}

        {/* occure only when verification have not pass courses */}
        {nonGraduateCheckResult &&
          nonGraduateCheckResult.not_pass_course.length != 0 && (
            <VerifyResult status={nonGraduateCheckResult.is_pass} />
          )}

        <div style={{ padding: "15px 0px" }} />

        <div className="verify-result-data">
          <div>
            {/* study result */}
            {graduateCheckResult && (
              <GradeResult gradeResult={graduateCheckResult.study_result} />
            )}

            {/* study result */}
            {nonGraduateCheckResult && (
              <GradeResult gradeResult={nonGraduateCheckResult} />
            )}
          </div>

          <div style={{ padding: "0px 20px" }} />

          <div className="other-verify-element">
            {/* occure only when verification have not pass courses */}
            {graduateCheckResult &&
              graduateCheckResult.study_result.not_pass_course.length === 0 && (
                <VerifyResult
                  status={
                    graduateCheckResult.fee_result &&
                    graduateCheckResult.activity_result &&
                    graduateCheckResult.study_result.is_pass
                  }
                />
              )}
            {/* occure only when verification have not pass courses */}
            {nonGraduateCheckResult &&
              nonGraduateCheckResult.not_pass_course.length === 0 && (
                <VerifyResult status={nonGraduateCheckResult.is_pass} />
              )}
            {/* fee and activity status */}
            {graduateCheckResult && (
              <div>
                <FeeActivityResult
                  label="สถานะการเข้าร่วมกิจกรรม"
                  status={graduateCheckResult.activity_result}
                />
                <FeeActivityResult
                  label="สถานะการชำระค่าธรรมเนียม"
                  status={graduateCheckResult.fee_result}
                />
              </div>
            )}

            {/* not pass courses */}
            {graduateCheckResult &&
              graduateCheckResult.study_result.not_pass_course.length != 0 && (
                <NotPassCourse
                  courses={graduateCheckResult.study_result.not_pass_course}
                />
              )}

            {/* not pass courses */}
            {nonGraduateCheckResult &&
              nonGraduateCheckResult.not_pass_course.length != 0 && (
                <NotPassCourse
                  courses={nonGraduateCheckResult.not_pass_course}
                />
              )}

            <Button
              className="resubmit"
              text="แนบไฟล์ใหม่"
              onClick={handleResubmitFile}
            ></Button>

            {graduateCheckResult && (
              <InspectorVerification status={graduateCheckResult.form_status} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function GradeResult({ gradeResult }: { gradeResult: StudyResult }) {
  return (
    <div className="grade-result">
      <GradeResultElement
        acquireCredit={gradeResult.acquired_credit}
        isPass={gradeResult.is_pass}
        lable="จำนวนหน่วยกิต"
        totalCredit={gradeResult.total_min_credit}
        isHeader={true}
      />
      <div className="category">
        {gradeResult.result.map((category) => (
          <div>
            <GradeResultElement
              acquireCredit={category.acquired_credit}
              isPass={category.is_pass}
              lable={category.category_name}
              totalCredit={category.total_min_credit}
            />
            <div className="subcategory">
              {category.subcategories.map((subcategory) => (
                <GradeResultElement
                  acquireCredit={subcategory.acquired_credit}
                  isPass={subcategory.is_pass}
                  lable={subcategory.subcategory_name}
                  totalCredit={subcategory.total_min_credit}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function GradeResultElement({
  isPass,
  lable,
  acquireCredit,
  totalCredit,
  isHeader = false,
}: {
  isPass: boolean;
  lable: string;
  acquireCredit: number;
  totalCredit: number;
  isHeader?: boolean;
}) {
  const mainDivClass = isHeader
    ? "category-lable study-verify-header"
    : "category-lable";

  return (
    <div className={mainDivClass}>
      {isPass ? (
        <div className="circle-green" />
      ) : (
        <div className="circle-red" />
      )}
      {lable}
      {`(${acquireCredit}/${totalCredit})`}
      {isHeader && (
        <a className="more-info" href={moreInfomationURL}>
          See more
        </a>
      )}
    </div>
  );
}

function VerifyResult({ status }: { status: boolean }) {
  const statusLabel = status ? "ผ่าน" : "ไม่ผ่าน";
  const color = status ? "status-pass" : "status-not-pass";
  const iconClass = status ? "verify-icon pass" : "verify-icon fail";

  return (
    <div className="verify-result">
      <div className={iconClass} />
      <div>
        <p className="label">Verified</p>
        <p className={color}>{statusLabel}</p>
      </div>
    </div>
  );
}

function InspectorVerification({ status }: { status: string }) {
  let iconClass = "form-status-icon pending";
  let statusLabel = "กำลังรอผู้ตรวจสอบยืนยันผลการตรวจสอบ";
  let style: string = "pending";

  if (status === "V") {
    iconClass = "form-status-icon verified";
    statusLabel = "ผ่านการตรวจสอบจากผู้ตรวจสอบ";
    style = "verify";
  }

  return (
    <div className={`form-status ${style}`}>
      <div className={iconClass} />
      <p>: {statusLabel}</p>
    </div>
  );
}

function NotPassCourse({ courses }: { courses: NotPassCourse[] }) {
  return (
    <div className="not-pass-course">
      <div className="warning-icon" />
      <p>วิชาที่ไม่ผ่านเกณฑ์</p>
      <div className="horizontal-space" />
      {courses.map((course) => (
        <div className="course">
          <p>{course.course_id}</p>
          <p>{course.course_name_th}</p>
          <p>{course.grade}</p>
        </div>
      ))}
    </div>
  );
}

function FeeActivityResult({
  status,
  label,
}: {
  status: boolean;
  label: string;
}) {
  return (
    <div className="fee-activity-result">
      <p>{label}</p>
      <div className={`${status ? "circle-green" : "circle-red"}`} />
    </div>
  );
}
