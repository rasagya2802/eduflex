import React, { useEffect, useState } from "react";

function Courses() {
  const [courses, setCourses] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  // Fetch courses
  useEffect(() => {
    fetch("http://localhost:8002/courses")
      .then((res) => res.json())
      .then((data) => setCourses(data))
      .catch((err) => console.error("Error fetching courses:", err));
  }, []);

  // Add a new course
  const handleSubmit = (e) => {
    e.preventDefault();
    fetch(`http://localhost:8002/courses?title=${title}&description=${description}`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((newCourse) => {
        setCourses([...courses, newCourse]);
        setTitle("");
        setDescription("");
      })
      .catch((err) => console.error("Error adding course:", err));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Course Management</h1>

      {/* Add Course Form */}
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Course Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ marginRight: "10px" }}
        />
        <input
          type="text"
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ marginRight: "10px" }}
        />
        <button type="submit">Add Course</button>
      </form>

      {/* Course List */}
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            <b>{course.title}</b>: {course.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Courses;
