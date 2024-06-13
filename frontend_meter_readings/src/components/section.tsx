import { ReactNode } from "react";

export default function Section({ children }: { children: ReactNode }) {
  return (
    <div className="p-2 row d-flex rounded align-items-center border flex-column gap-2">
      {children}
    </div>
  );
}
