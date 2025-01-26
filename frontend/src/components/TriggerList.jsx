import React from "react";

const TriggerList = () => {
  const mockTriggers = [
    { id: 1, type: "scheduled", details: "Every 10 minutes" },
    { id: 2, type: "api", details: '{"key": "value"}' },
  ];

  return (
    <div>
      <h2>Created Triggers</h2>
      <ul>
        {mockTriggers.map((trigger) => (
          <li key={trigger.id}>
            <strong>Type:</strong> {trigger.type}, <strong>Details:</strong> {trigger.details}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TriggerList;
