import { useState } from "react";
import Section from "../components/section";
import axios from "axios";

export default function ExecuteSQL({ taskId }: { taskId: string }) {
  const hasTaskId = Boolean(taskId);
  const [isLoading, setIsLoading] = useState(false);
  return (
    <form
      target="_blank"
      onSubmit={async (e) => {
        e.preventDefault();
        try {
          setIsLoading(true);
          await axios.post("http://localhost:5000/execute-sql", {
            task_id: taskId,
          });
        } catch (e) {
          console.error(e);
        } finally {
          setIsLoading(false);
        }
      }}
    >
      <Section>
        {hasTaskId ? (
          <>
            <label htmlFor="execute">
              Step 3. Task ID is {taskId}. You can execute the SQL
            </label>
            <div className="row w-50">
              <input
                className="btn btn-success"
                id="execute"
                type="submit"
                value="Execute SQL"
              />
            </div>
            {isLoading && <div className="spinner-border" role="status"></div>}
          </>
        ) : (
          <p>Step 3. Please upload a file to begin</p>
        )}
      </Section>
    </form>
  );
}
