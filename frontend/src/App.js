import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [courses, setCourses] = useState([]);
  const [newCourse, setNewCourse] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8003/courses")
      .then(res => setCourses(res.data))
      .catch(err => console.error(err));
  }, []);

  const addCourse = () => {
    axios.post(`http://localhost:8003/courses?name=${newCourse}&description=Sample`)
      .then(() => window.location.reload())
      .catch(err => console.error(err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>EduFlex - Courses</h1>
      <input 
        value={newCourse} 
        onChange={(e) => setNewCourse(e.target.value)} 
        placeholder="Course name" 
      />
      <button onClick={addCourse}>Add Course</button>
      <ul>
        {courses.map(c => <li key={c.id}>{c.name} - {c.description}</li>)}
      </ul>
    </div>
  );
}

export default App;
