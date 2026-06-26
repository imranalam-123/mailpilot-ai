import { useEffect, useState } from "react";
import api from "../api/api";

function Templates() {
  const [templates, setTemplates] = useState([]);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await api.get("/my-templates", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });

      setTemplates(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load templates");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#0f172a",
        color: "white",
        padding: "40px",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px",
        }}
      >
        Custom Templates
      </h1>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr>
            <th style={thStyle}>ID</th>
            <th style={thStyle}>Name</th>
            <th style={thStyle}>Description</th>
            <th style={thStyle}>Sample Prompt</th>
            <th style={thStyle}>Actions</th>
          </tr>
        </thead>

        <tbody>
          {templates.map((template) => (
            <tr key={template.id}>
              <td style={tdStyle}>{template.id}</td>

              <td style={tdStyle}>{template.name}</td>

              <td style={tdStyle}>
                {template.description}
              </td>

              <td style={tdStyle}>
                {template.sample_prompt}
              </td>

              <td style={tdStyle}>
                <button>Edit</button>{" "}
                <button>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {templates.length === 0 && (
        <h3
          style={{
            textAlign: "center",
            marginTop: "30px",
          }}
        >
          No Templates Found
        </h3>
      )}
    </div>
  );
}

const thStyle = {
  border: "1px solid #334155",
  padding: "12px",
  backgroundColor: "#1e293b",
};

const tdStyle = {
  border: "1px solid #334155",
  padding: "12px",
  textAlign: "center",
};

export default Templates;