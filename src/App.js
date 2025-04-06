import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import "./App.css";
import Trail from "./componets/Trail";
import Login from "./componets/login";
import Dashboard from "./componets/Dashboard";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [customerID, setCustomerID] = useState("");

  const handleLoginSuccess = (id) => {
    setCustomerID(id);
    setIsAuthenticated(true);
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Public route - login page */}
          <Route
            path="/login"
            element={
              isAuthenticated ? (
                <Navigate to="/dashboard" />
              ) : (
                <Login onLoginSuccess={handleLoginSuccess} />
              )
            }
          />

          {/* Protected route - dashboard */}
          <Route
            path="/dashboard"
            element={
              isAuthenticated ? (
                <Dashboard customerID={customerID} />
              ) : (
                <Navigate to="/login" />
              )
            }
          />

          {/* Default redirect */}
          <Route
            path="/"
            element={
              <Navigate to={isAuthenticated ? "/dashboard" : "/login"} />
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
