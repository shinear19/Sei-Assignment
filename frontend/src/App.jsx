import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css"; // Import custom CSS

function App() {
  const [triggers, setTriggers] = useState([]);
  const [newTrigger, setNewTrigger] = useState({
    type: "",
    time: "",
    payload: "",
  });
  const [events, setEvents] = useState([]);

  // Fetch triggers and events
  useEffect(() => {
    // Fetch triggers
    axios
      .get("http://localhost:5000/api/triggers")
      .then((response) => {
        setTriggers(response.data);
      })
      .catch((error) => {
        console.error("Error fetching triggers:", error);
      });

    // Fetch events
    axios
      .get("http://localhost:5000/api/events")
      .then((response) => {
        setEvents(response.data);
      })
      .catch((error) => {
        console.error("Error fetching events:", error);
      });
  }, []);

  const handleCreateTrigger = () => {
    // Send POST request to create a new trigger
    axios
      .post("http://localhost:5000/api/triggers", newTrigger)
      .then((response) => {
        setTriggers([...triggers, response.data]);
        setNewTrigger({ type: "", time: "", payload: "" });
      })
      .catch((error) => {
        console.error("Error creating trigger:", error);
      });
  };

  const handleTestTrigger = (triggerId) => {
    // Test an existing trigger
    axios
      .post("http://localhost:5000/api/test-trigger", { trigger_id: triggerId })
      .then(() => {
        alert("Trigger tested successfully!");
      })
      .catch((error) => {
        console.error("Error testing trigger:", error);
      });
  };

  return (
    <div className="app-container">
      <h1 className="title">Segwise - Event Trigger Platform</h1>

      {/* Create Trigger Form */}
      <div className="form-container">
        <h2>Create Trigger</h2>
        <div className="form-inputs">
          <input
            type="text"
            placeholder="Type (scheduled/api)"
            value={newTrigger.type}
            onChange={(e) => setNewTrigger({ ...newTrigger, type: e.target.value })}
            className="input"
          />
          <input
            type="text"
            placeholder="Time"
            value={newTrigger.time}
            onChange={(e) => setNewTrigger({ ...newTrigger, time: e.target.value })}
            className="input"
          />
          <input
            type="text"
            placeholder="Payload"
            value={newTrigger.payload}
            onChange={(e) => setNewTrigger({ ...newTrigger, payload: e.target.value })}
            className="input"
          />
          <button className="btn" onClick={handleCreateTrigger}>Create Trigger</button>
        </div>
      </div>

      {/* Display Triggers */}
      <div className="list-container">
        <h2>Triggers</h2>
        <ul className="list">
          {triggers.map((trigger) => (
            <li key={trigger.trigger_id} className="list-item">
              <span>{trigger.type} - {trigger.time}</span>
              <button
                onClick={() => handleTestTrigger(trigger.trigger_id)}
                className="btn test-btn"
              >
                Test Trigger
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* Display Events */}
      <div className="list-container">
        <h2>Events</h2>
        <ul className="list">
          {events.map((event) => (
            <li key={event.event_id} className="list-item">
              Event triggered for {event.trigger_id} with status {event.status}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
