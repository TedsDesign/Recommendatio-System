import React, { useState } from "react";
import "./login.css";
import Dashboard from "./Dashboard";

function Login() {
  const [customerID, setCustomerID] = useState("");
  const [customerData, setCustomerData] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    console.log("Login with Customer ID: ", { customerID });
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ customerID }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Login Failed");
      }

      setCustomerData(data);
      setIsAuthenticated(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      {isAuthenticated ? (
        <Dashboard customerID={customerID} />
      ) : (
        <div className="login-box">
          <h2>Enter your Customer ID</h2>
          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="customerID">Customer ID</label>
              <input
                type="text"
                id="customer_ID"
                onChange={(e) => {
                  setCustomerID(e.target.value);
                }}
                required
              />
              <button type="submit" className="login-button">
                Submit
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default Login;
