import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api/api";

function EmailPreview() {
  const location = useLocation();
  const navigate = useNavigate();

  const { email, recipient, subject } = location.state || {};

  const [editedEmail, setEditedEmail] = useState(email || "");

  const handleSend = async () => {
    try {
      await api.post("/send-email", {
        to_email: recipient,
        subject: subject || "AI Generated Email",
        body: editedEmail,
      });

      alert("Email Sent Successfully!");

      navigate("/history");
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Failed to send email");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        padding: "40px",
        color: "white",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px",
        }}
      >
        Email Preview
      </h1>

      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
        }}
      >
        <p>
          <strong>Recipient:</strong> {recipient}
        </p>

        <p>
          <strong>Subject:</strong>{" "}
          {subject || "AI Generated Email"}
        </p>

        <textarea
          value={editedEmail}
          onChange={(e) =>
            setEditedEmail(e.target.value)
          }
          rows={18}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "15px",
            borderRadius: "10px",
            fontSize: "15px",
            background: "#1e293b",
            color: "white",
          }}
        />

        <button
          onClick={handleSend}
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "15px",
            border: "none",
            borderRadius: "10px",
            background: "#2563eb",
            color: "white",
            fontSize: "18px",
            cursor: "pointer",
          }}
        >
          Send Email
        </button>
      </div>
    </div>
  );
}

export default EmailPreview;