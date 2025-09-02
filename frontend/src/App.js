import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [courses, setCourses] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [editId, setEditId] = useState(null); // track course being edited

  const API_URL = "http://localhost:8002/courses"; // backend

  // Fetch all courses
  const fetchCourses = async () => {
    try {
      const res = await axios.get(API_URL);
      setCourses(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  // Add new course
  const addCourse = async () => {
    try {
      await axios.post(API_URL, { title, description });
      setTitle("");
      setDescription("");
      fetchCourses();
    } catch (err) {
      console.error(err);
    }
  };

  // Delete course
  const deleteCourse = async (id) => {
    try {
      await axios.delete(`${API_URL}/${id}`);
      fetchCourses();
    } catch (err) {
      console.error(err);
    }
  };

  // Start editing a course
  const startEdit = (course) => {
    setEditId(course.id);
    setTitle(course.title);
    setDescription(course.description);
  };

  // Update course
  const updateCourse = async () => {
    try {
      await axios.put(`${API_URL}/${editId}`, { title, description });
      setEditId(null);
      setTitle("");
      setDescription("");
      fetchCourses();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>📚 Course Management</h2>

      <div>
        <input
          type="text"
          placeholder="Course Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          type="text"
          placeholder="Course Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        {editId ? (
          <button onClick={updateCourse}>Update Course</button>
        ) : (
          <button onClick={addCourse}>Add Course</button>
        )}
      </div>

      <h3>All Courses</h3>
      <ul>
        {courses.map((c) => (
          <li key={c.id}>
            <strong>{c.title}</strong> - {c.description}
            <button
              onClick={() => deleteCourse(c.id)}
              style={{ marginLeft: "10px" }}
            >
              Delete
            </button>
            <button
              onClick={() => startEdit(c)}
              style={{ marginLeft: "10px" }}
            >
              Edit
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
