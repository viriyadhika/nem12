import { useState } from "react";
import UploadFile from "./meter-readings/upload-file";
import DownloadResult from "./meter-readings/download-result";

function App() {
  const [taskId, setTaskId] = useState("");

  return (
    <div className="container py-5">
      <div className="d-flex flex-column gap-4">
        <UploadFile onUploaded={setTaskId} />
        <DownloadResult taskId={taskId} />
      </div>
    </div>
  );
}

export default App;
