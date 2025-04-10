import React, { useState } from "react";
import axios from "axios";
import { useGlobalContext } from "../../contexts/baseContext";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { backendURL, setBackendUrl } = useGlobalContext();

  const styles = "border-3 border-light-gray-200 m-4 rounded";
  const mod = "login-";
  let access = "default";
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      console.log("attempting login with email ", email);
      console.log(" and password: ", password);
      console.log(backendURL);
      const loginURL = backendURL + "api/login";
      console.log("posting to ", loginURL);
      const response = await axios.post(loginURL, {
        email: email,
        password: password,
      });
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      //maybe this should be something else.
      window.location.href = "/treasures";
      // Handle successful login (e.g., redirect, show success message)
      console.log("Login successful: for ", email);
      access = response.data.access;
    } catch (error) {
      // Handle error (e.g., show error message)
      console.error("Login failed:", error);
      if (error.response) {
        console.log(error.response.data);
        setError(error.response.data.detail);
      }
      if (error.request) {
        console.log(error.request);
      }
      if (error.message) {
        console.log(error.message);
      }
      console.log(error.config);
    }
  };
  return (
    <div>
      <h3>Login</h3>
      <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
        <form onSubmit={handleLogin}>
          <label htmlFor={mod + "email"} className="whitespace-nowrap">
            Email:
          </label>
          <input
            type="email"
            name={mod + "email"}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id={mod + "email"}
            placeholder="Email"
            required
            className={styles}
          />
          <label htmlFor={mod + "password"} className="whitespace-nowrap">
            Password:
          </label>
          <input
            type="password"
            name={mod + "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id={mod + "password"}
            placeholder="Password"
            required
            className={styles}
          />
          <button type="submit">Login</button>
        </form>
        {error && <p>{error}</p>}
      </div>
      <div>
        <p>{access}</p>
      </div>
    </div>
  );
};

export default LoginForm;
