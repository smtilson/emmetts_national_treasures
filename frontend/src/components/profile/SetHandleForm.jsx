import axios from "axios";
import { useState, useEffect } from "react";
import { useGlobalContext } from "../../contexts/baseContext";
import { useNavigate } from "react-router-dom";

function SetHandleForm() {
  return <h2>Not yet implemented</h2>;
  /*
    const {backendURL, isAuthenticated, user} = useGlobalContext();
    const navigate = useNavigate();
    const [handle, setHandle] = useState(user.handle ? user.handle : "");
    const [error, setError] = useState("");
    const [successMessage, setSuccessMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(backendURL + "api/set_handle/", {handle});
            setUser(response.data);
            setSuccessMessage("Handle set successfully!");
            navigate("/");
        } catch (error) {
            setError("Error setting handle. Please try again.");
        }
    }
    return (
        <>
        <h3>Unimplemented Form</h3>
        </>
    )*/
}

export default SetHandleForm;
