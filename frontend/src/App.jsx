import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import GenerateEmail from "./pages/GenerateEmail";
import EmailPreview from "./pages/EmailPreview";
import History from "./pages/History";
import Templates from "./pages/Templates";
import Stats from "./pages/Stats";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/generate"
          element={<GenerateEmail />}
        />

        {/* NEW ROUTE */}
        <Route
          path="/preview"
          element={<EmailPreview />}
        />

        <Route
          path="/history"
          element={<History />}
        />

        <Route
          path="/templates"
          element={<Templates />}
        />

        <Route
          path="/stats"
          element={<Stats />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;