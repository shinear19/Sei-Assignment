import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/api";

// Create a trigger
export const createTrigger = (data) => axios.post(`${API_BASE_URL}/triggers/`, data);

// Get all triggers
export const getTriggers = () => axios.get(`${API_BASE_URL}/triggers/`);

// Delete a trigger
export const deleteTrigger = (id) => axios.delete(`${API_BASE_URL}/triggers/${id}/`);

// Get logs
export const getLogs = (filter) => axios.get(`${API_BASE_URL}/logs/`, { params: { filter } });
