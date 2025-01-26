import React, { useState } from "react";

const TriggerForm = ({ onTriggerCreated }) => {
  const [triggerType, setTriggerType] = useState("scheduled");
  const [triggerDetails, setTriggerDetails] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(`Trigger Type: ${triggerType}, Details: ${triggerDetails}`);
    // Call API or function to save trigger
    if (onTriggerCreated) onTriggerCreated();
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
      <label>
        Trigger Type:
        <select
          value={triggerType}
          onChange={(e) => setTriggerType(e.target.value)}
          style={{ marginLeft: "10px", marginBottom: "10px" }}
        >
          <option value="scheduled">Scheduled</option>
          <option value="api">API</option>
        </select>
      </label>
      <br />
      <label>
        Trigger Details:
        <input
          type="text"
          value={triggerDetails}
          onChange={(e) => setTriggerDetails(e.target.value)}
          placeholder="Enter details..."
          style={{
            marginLeft: "10px",
            padding: "5px",
            width: "300px",
            marginBottom: "10px",
          }}
        />
      </label>
      <br />
      <button type="submit" style={{ padding: "10px 20px", cursor: "pointer" }}>
        Create Trigger
      </button>
    </form>
  );
};

export default TriggerForm;
