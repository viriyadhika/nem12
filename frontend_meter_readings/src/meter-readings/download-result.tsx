import Section from "../components/section";

export default function DownloadResult({ taskId }: { taskId: string }) {
  const hasTaskId = Boolean(taskId);

  return (
    <form action={`http://localhost:5000/get-result/${taskId}`} target="_blank">
      <Section>
        {hasTaskId ? (
          <>
            <label htmlFor="download">
              Step 2. Task ID is {taskId}. You can now download result
            </label>
            <div className="row w-50">
              <input
                className="btn btn-success"
                id="download"
                type="submit"
                value="Download result"
              />
            </div>
          </>
        ) : (
          <p>Step 2. Please upload a file to begin</p>
        )}
      </Section>
    </form>
  );
}
