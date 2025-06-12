import {
  EmailInput,
  PasswordInput,
  ConfirmPasswordInput,
  TextInput,
} from "../forms/Inputs";
import { useState } from "react";
import { useGlobalContext } from "../../contexts/baseContext";
import axios from "axios";

function SignUp() {
  let styles = "border-2 border-light-gray-300 m-4 rounded";
  return (
    <div>
      <h3>Sign Up</h3>
      <form action="" className="signup-form flex flex-col space-y-4">
        <EmailInput styles={styles} modifier={"signup"} />
        <TextInput
          styles={styles}
          label={"Handle:"}
          name={"handle"}
          placeholder={"Handle"}
          id={"handle"}
        />
        <PasswordInput styles={styles} modifier={"signup"} />
        <ConfirmPasswordInput styles={styles} modifier={"signup"} />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

const SignUpForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [handle, setHandle] = useState("");
  const [passwordMatch, setPasswordMatch] = useState(false);
  const [error, setError] = useState("");
  const { backendURL, setUser, setIsAuthenticated } = useGlobalContext();
  //const navigate = useNavigate();

  /*const validatePasswords = () => {
    setPasswordMatch(password === confirmPassword);
    return password === confirmPassword;
  };*/

  const styles = "border-3 border-light-gray-200 m-4 rounded";
  const mod = "signup-";
  const checkPasswords = (password, confirmPassword) => {
    let match;
    if (password === confirmPassword) {
      match = true;
    } else {
      match = false;
      setError("Passwords do not match");
    }
    setPasswordMatch(match);
  };
  const handleSignUp = async (e) => {
    e.preventDefault();
    checkPasswords(password, confirmPassword);
    if (!passwordMatch) {
      return;
    }
    // how do I get this to display something though?
    try {
      // Logging for debuging
      console.log("attempting signup with email ", email);
      const signUpURL = backendURL + "api/signup/";
      console.log("posting to ", signUpURL);
      //console.log("data: \n");
      //console.log("email: ", email);
      //console.log("password: ", password);
      //console.log("confirm_password: ", confirmPassword);
      //console.log("handle: ", handle);
      const response = await axios.post(signUpURL, {
        email: email,
        password: password,
        confirm_password: confirmPassword,
        handle: handle,
      });
      
      // storing tokens in local storage
      localStorage.setItem("accessToken", response.data.access);
      localStorage.setItem("refreshToken", response.data.refresh);
      const userId = response.data.id;
      console.log("attempting to retrieve user data for userId ", userId);
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
      console.error("Sign up failed:", error);
      setIsAuthenticated(false);
      setUser(null);
      
      // Enhanced error logging
      console.log("Error details:", {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
      });
      
      if (error.response) {
        console.log("Full error response:", error.response);
        
        // Check for errors in the errors field first
        if (error.response.data.errors) {
          if (error.response.data.errors.email) {
            setError(error.response.data.errors.email[0]);
          } else if (error.response.data.errors.password) {
            setError(error.response.data.errors.password[0]);
          } else if (error.response.data.errors.handle) {
            setError(error.response.data.errors.handle[0]);
          } else {
            // If no specific field error, use the detail
            setError(error.response.data.detail);
          }
        } else if (error.response.data.detail) {
          setError(error.response.data.detail);
        } else {
          setError("Signup failed, an unknown error occurred");
        }
      } else {
        setError("Network error. Please check your connection and try again.");
      }
    }
    const refreshToken = localStorage.getItem("refreshToken");
    return refreshToken;
  };
  return (
    <div>
      <h3>Sign Up</h3>
      <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
        <form onSubmit={handleSignUp}>
          <span>
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
          </span>
          <span>
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
          </span>
          <span>
            <label
              htmlFor={mod + "confirm-password"}
              className="whitespace-nowrap"
            >
              Confirm Password:
            </label>
            <input
              type="password"
              name={mod + "confirm-password"}
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              id={mod + "confirm-password"}
              placeholder="Confirm Password"
              required
              className={`border-3 m-4 rounded ${
                !passwordMatch ? "border-red-500" : "border-light-gray-200"
              }`}
            />
            {!passwordMatch && <p>Passwords do not match.</p>}
            <span>
              <label htmlFor={mod + "handle"} className="whitespace-nowrap">
                Handle:
              </label>
              <input
                type="text"
                name={mod + "handle"}
                value={handle}
                onChange={(e) => setHandle(e.target.value)}
                id={mod + "handle"}
                placeholder="Handle"
                className={styles}
              />
            </span>
          </span>

          <button
            type="submit"
            disabled={!password || !email || !confirmPassword}
          >
            Sign Up
          </button>
        </form>
        {error && <p className="text-red-500">{error}</p>}
      </div>
      <p>{email}</p>
    </div>
  );
};

export default SignUpForm;
