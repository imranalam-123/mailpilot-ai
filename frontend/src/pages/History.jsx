import { useEffect, useState } from "react";
import api from "../api/api";

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get("/email-history", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem(
            "token"
          )}`,
        },
      });

      setHistory(response.data);
    } catch (error) {
      console.error(error);
      alert("Failed to load email history");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <h2
        style={{
          textAlign: "center",
          color: "white",
          marginTop: "50px",
        }}
      >
        Loading...
      </h2>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#0f172a",
        padding: "30px",
        color: "white",
      }}
    >
      <h1
        style={{
          textAlign: "center",
          marginBottom: "30px",
        }}
      >
        Email History
      </h1>

      <div
        style={{
          overflowX: "auto",
        }}
      >
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            backgroundColor: "#111827",
          }}
        >
          <thead>
            <tr>
              <th style={thStyle}>ID</th>
              <th style={thStyle}>Prompt</th>
              <th style={thStyle}>Email Type</th>
              <th style={thStyle}>Created At</th>
              <th style={thStyle}>View Email</th>
            </tr>
          </thead>

          <tbody>
            {history.map((email) => (
              <tr key={email.id}>
                <td style={tdStyle}>{email.id}</td>

                <td style={tdStyle}>
                  {email.prompt}
                </td>

                <td style={tdStyle}>
                  {email.email_type}
                </td>

                <td style={tdStyle}>
                  {new Date(
                    email.created_at
                  ).toLocaleString()}
                </td>

                <td style={tdStyle}>
                  <button
                    onClick={() =>
                      alert(email.generated_email)
                    }
                    style={{
                      padding: "8px 12px",
                      backgroundColor: "#2563eb",
                      color: "white",
                      border: "none",
                      borderRadius: "6px",
                      cursor: "pointer",
                    }}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {history.length === 0 && (
          <h3
            style={{
              textAlign: "center",
              marginTop: "30px",
            }}
          >
            No Email History Found
          </h3>
        )}
      </div>
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

export default History;