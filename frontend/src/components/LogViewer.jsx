import React from "react";

const LogViewer = () => {
  const mockLogs = [
    { id: 1, type: "scheduled", time: "2025-01-24 14:00", details: "Fired at 2 PM" },
    { id: 2, type: "api", time: "2025-01-24 14:30", details: '{"key": "value"}' },
  ];

  return (
    <div style={{ marginTop: "20px" }}>
      <h2>Event Logs</h2>
      <ul>
        {mockLogs.map((log) => (
          <li key={log.id}>
            <strong>Type:</strong> {log.type}, <strong>Time:</strong> {log.time},{" "}
            <strong>Details:</strong> {log.details}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LogViewer;
