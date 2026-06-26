import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function GenerateEmail() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    to_email: "",
    email_type: "leave",
    tone: "formal",
    template: "sick_leave",
    prompt: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleGenerate = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      const response = await api.post(
        "/generate-email",
        formData
      );

      navigate("/preview", {
        state: {
          recipient: formData.to_email,
          subject:
            response.data.subject ||
            `${formData.email_type} Email`,
          email: response.data.generated_email,
        },
      });
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail ||
          "Failed to generate email."
      );
    } finally {
      setLoading(false);
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
          marginBottom: "30px",
        }}
      >
        Generate & Preview Email
      </h1>

      <form
        onSubmit={handleGenerate}
        style={{
          maxWidth: "700px",
        }}
      >
        <input
          type="email"
          name="to_email"
          placeholder="Recipient Email"
          value={formData.to_email}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <select
          name="email_type"
          value={formData.email_type}
          onChange={handleChange}
          style={inputStyle}
        >
          <option value="leave">Leave</option>
          <option value="meeting">Meeting</option>
          <option value="job_application">
            Job Application
          </option>
        </select>

        <select
          name="tone"
          value={formData.tone}
          onChange={handleChange}
          style={inputStyle}
        >
          <option value="formal">Formal</option>
          <option value="friendly">Friendly</option>
          <option value="professional">
            Professional
          </option>
        </select>

        <input
          type="text"
          name="template"
          placeholder="Template"
          value={formData.template}
          onChange={handleChange}
          style={inputStyle}
        />

        <textarea
          name="prompt"
          rows="6"
          placeholder="Describe the email..."
          value={formData.prompt}
          onChange={handleChange}
          required
          style={inputStyle}
        />

        <button
          type="submit"
          disabled={loading}
          style={buttonStyle}
        >
          {loading
            ? "Generating..."
            : "Generate Preview"}
        </button>
      </form>
    </div>
  );
}

const inputStyle = {
  width: "100%",
  padding: "12px",
  marginBottom: "15px",
  borderRadius: "8px",
  border: "1px solid #475569",
  backgroundColor: "#1e293b",
  color: "white",
  fontSize: "15px",
};

const buttonStyle = {
  width: "100%",
  padding: "14px",
  border: "none",
  borderRadius: "8px",
  backgroundColor: "#2563eb",
  color: "white",
  cursor: "pointer",
  fontSize: "16px",
  fontWeight: "bold",
};

export default GenerateEmail;