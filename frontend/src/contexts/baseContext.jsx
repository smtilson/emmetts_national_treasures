import React, { createContext, useContext, useState } from "react";

const GlobalContext = createContext();

export const GlobalProvider = ({ children }) => {
  const [backendURL, setBackendURL] = useState("http://127.0.0.1:8000/");
  return (
    <GlobalContext.Provider value={{ backendURL, setBackendURL }}>
      {children}
    </GlobalContext.Provider>
  );
};

export const useGlobalContext = () => useContext(GlobalContext);
