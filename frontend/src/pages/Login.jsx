import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const formData = new URLSearchParams();

      formData.append("username", email);
      formData.append("password", password);

      const response = await api.post(
        "/login",
        formData,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem(
        "token",
        response.data.access_token
      );

      alert("Login Successful");

      navigate("/dashboard");
    } catch (error) {
      console.error(error);

      alert(
        error.response?.data?.detail ||
        "Login Failed"
      );
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        backgroundColor: "#0f172a",
      }}
    >
      <form
        onSubmit={handleLogin}
        style={{
          width: "400px",
          padding: "30px",
          borderRadius: "12px",
          border: "1px solid #334155",
          backgroundColor: "#111827",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            marginBottom: "30px",
            color: "white",
          }}
        >
          MailPilot AI
        </h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
          required
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "15px",
            borderRadius: "6px",
            border: "1px solid #475569",
            backgroundColor: "#1e293b",
            color: "white",
          }}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
          required
          style={{
            width: "100%",
            padding: "12px",
            marginBottom: "20px",
            borderRadius: "6px",
            border: "1px solid #475569",
            backgroundColor: "#1e293b",
            color: "white",
          }}
        />

        <button
          type="submit"
          style={{
            width: "100%",
            padding: "12px",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
            backgroundColor: "#2563eb",
            color: "white",
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;