import React, { useState, useEffect } from "react";
import { useGlobalContext } from "../../contexts/baseContext";
import SetHandleForm from "./SetHandleForm";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Profile() {
  const { user, backendURL, isAuthenticated } = useGlobalContext();
  const [userDetails, setUserDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/login");
      return;
    }
    const fetchUserDetails = async () => {
      try {
        const accessToken = localStorage.getItem("accessToken");
        console.log("stored access token " + accessToken);
        console.log("user.id " + user.id);
        console.log("typeof user.id " + typeof user.id);
        if (!accessToken) {
          console.log("No access token found in local storage.");
          setError("No access token found in local storage.");
          setLoading(false);
          return;
        }
        const response = await axios.get(backendURL + "api/users/" + user.id, {
          headers: { Authorization: "Bearer " + accessToken },
        });
        setUserDetails(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching user details:", error);
        setError("Failed to load user details.");
        setLoading(false);
      }
    };

    if (isAuthenticated && user) {
      fetchUserDetails();
    } else {
      setLoading(false);
    }
  }, [user, backendURL, isAuthenticated, navigate]);

  if (loading) {
    return <div>Loading Profile...</div>;
  }
  if (error) {
    return <div className="text-red-500">{error}</div>;
  }
  if (!isAuthenticated) {
    return <div>Please log in.</div>;
  }
  return (
    <div>
      <h1>Welcome {user.email}</h1>
      <SetHandleForm />
    </div>
  );
}

export default Profile;
