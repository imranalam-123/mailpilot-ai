import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        color: "white",
        padding: "30px",
      }}
    >
      <h1>MailPilot AI Dashboard</h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3,1fr)",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <Link to="/generate">
          <button style={cardStyle}>
            Generate & Send Email
          </button>
        </Link>

        <Link to="/history">
          <button style={cardStyle}>
            Email History
          </button>
        </Link>

        <Link to="/templates">
          <button style={cardStyle}>
            Templates
          </button>
        </Link>

        <Link to="/stats">
          <button style={cardStyle}>
            Statistics
          </button>
        </Link>
      </div>
    </div>
  );
}

const cardStyle = {
  width: "100%",
  height: "120px",
  borderRadius: "12px",
  border: "none",
  background: "#2563eb",
  color: "white",
  fontSize: "18px",
  cursor: "pointer",
};

export default Dashboard;