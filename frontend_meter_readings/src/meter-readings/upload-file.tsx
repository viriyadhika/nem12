import { useState } from "react";
import axios from "axios";
import Section from "../components/section";

type UploadResult = {
  task_id: string;
};

export type UploadFileProps = {
  onUploaded: (task_id: string) => void;
};

export default function UploadFile({ onUploaded }: UploadFileProps) {
  const [file, setFile] = useState<File | null>(null);
  return (
    <form
      method="POST"
      encType="multipart/form-data"
      onSubmit={async (e) => {
        e.preventDefault();
        if (file) {
          const formData = new FormData();
          formData.append("file", file);
          try {
            const res = await axios.post<UploadResult>(
              "http://localhost:5000/upload",
              formData
            );
            onUploaded(res.data.task_id);
          } catch (e) {
            console.error(e);
          }
        }
      }}
    >
      <Section>
        <label htmlFor="formFile" className="form-label">
          Step 1. Choose csv file to upload
        </label>
        <div className="row w-50">
          <input
            type="file"
            name="file"
            accept=".csv"
            id="formFile"
            className="form-control"
            onChange={(e) => {
              if (e.target.files) {
                setFile(e.target.files[0]);
              }
            }}
          />
        </div>
        <div className="row w-50">
          <input type="submit" className="btn btn-success" value="Upload" />
        </div>
      </Section>
    </form>
  );
}
