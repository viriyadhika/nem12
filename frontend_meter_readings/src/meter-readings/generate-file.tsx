import { useState } from "react";
import axios from "axios";
import Section from "../components/section";

type UploadResult = {
  task_id: string;
};

export default function GenerateFile() {
  const [size, setSize] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  return (
    <form
      method="POST"
      encType="multipart/form-data"
      onSubmit={async (e) => {
        e.preventDefault();
        if (Number(size) > 0 && Number(size) <= 5000) {
          const castedInt = Math.floor(Number(size));
          try {
            setIsLoading(true);
            const res = await axios.post<UploadResult>(
              "http://localhost:5000/generate-file",
              { size: castedInt }
            );
            window.open(
              `http://localhost:5000/get-mock-result/${res.data.task_id}`,
              "_blank"
            );
          } catch (e) {
            console.error(e);
          } finally {
            setIsLoading(false);
          }
        } else {
          alert("Input a number between 0 to 5000");
        }
      }}
    >
      <Section>
        <label htmlFor="generateFile" className="form-label">
          Step 0. Generate file (optional)
        </label>
        <div className="d-flex w-50">
          <input
            type="number"
            id="generateFile"
            className="form-control"
            placeholder="Input number of rows to be generated between 1 to 5000"
            value={size}
            onChange={(e) => {
              const casted = Number(e.target.value);
              if (isNaN(casted)) {
                return;
              }
              setSize(e.target.value);
            }}
          />
        </div>
        <div className="row w-50">
          <input type="submit" className="btn btn-success" value="Generate" />
        </div>
        {isLoading && <div className="spinner-border" role="status"></div>}
      </Section>
    </form>
  );
}
