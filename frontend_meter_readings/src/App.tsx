import { useState } from "react";
import UploadFile from "./meter-readings/upload-file";
import DownloadResult from "./meter-readings/download-result";
import GenerateFile from "./meter-readings/generate-file";
import ExecuteSQL from "./meter-readings/execute-sql";

function App() {
  const [taskId, setTaskId] = useState("");

  return (
    <div className="container py-5">
      <div className="d-flex flex-column gap-4">
        <h2>NEM12 Parser</h2>
        <GenerateFile />
        <UploadFile onUploaded={setTaskId} />
        <DownloadResult taskId={taskId} />
        <ExecuteSQL taskId={taskId} />
      </div>
    </div>
  );
}

export default App;
