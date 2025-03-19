import React, { useState } from "react";
import "../styles/uploadfile-button.css";
import { IoCloudUploadOutline, IoCloseCircleOutline } from "react-icons/io5";

interface UploadFileButtonProps {
  onChange?: (event: React.ChangeEvent<HTMLInputElement>) => void;
  buttonText?: string;
  onRemoveFile?: () => void;
}

const UploadFileButton: React.FC<UploadFileButtonProps> = ({
  onChange,
  buttonText = "แนบไฟล์",
  onRemoveFile,
}) => {
  const [fileName, setFileName] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const truncatedName =
        file.name.length > 15
          ? `${file.name.substring(0, 12)}...${file.name.split(".").pop()}`
          : file.name;
      setFileName(truncatedName);
      if (onChange) {
        onChange(event);
      }
    }
  };

  const handleRemoveFile = () => {
    setFileName(null);
    if (onRemoveFile) {
      onRemoveFile();
    }
  };

  return (
    <div className="upload-file-button">
      <label className={"uploadfile-button"}>
        {!fileName && <IoCloudUploadOutline className="upload-icon" />}
        {fileName || buttonText}
        <input
          type="file"
          onChange={handleFileChange}
          key={fileName} 
        />
      </label>
      {fileName && (
        <IoCloseCircleOutline
          className="delete-icon"
          onClick={handleRemoveFile}
        />
      )}
    </div>
  );
};

export default UploadFileButton;
