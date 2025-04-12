import { useState } from "react";
import axios from "axios";
import { useGlobalContext } from "../../contexts/baseContext";
//import {useNavigate} from "react-router-dom";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { backendURL, setUser, setIsAuthenticated } = useGlobalContext();
  //const navigate = useNavigate();

  const styles = "border-3 border-light-gray-200 m-4 rounded";
  const mod = "login-";
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Logging for debuging
      console.log("attempting login with email ", email);
      console.log(" and password: ", password);
      console.log(backendURL);
      const loginURL = backendURL + "api/login/";
      console.log("posting to ", loginURL);
      const response = await axios.post(loginURL, {
        email: email,
        password: password,
      });
      console.log("Login successful: for ", email);
      // storing tokens in local storage
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      const userId = response.data.id;
      console.log("user logged in with id ", userId);
      console.log("access token ", response.data.access);

      const userResponse = await axios.get(backendURL + "api/users/" + userId, {
        headers: {
          Authorization: "Bearer " + response.data.access,
        },
      });
      console.log("User response: ", userResponse.data);
      setUser(userResponse.data);
      setIsAuthenticated(true);
    } catch (error) {
      // Handle error (e.g., show error message)
      console.error("Login failed:", error);
      setIsAuthenticated(false);
      setUser(null);
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
    const refreshToken = localStorage.getItem("refreshToken");
    return refreshToken;
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
        <p>{email}</p>
      </div>
    </div>
  );
};

export default LoginForm;
