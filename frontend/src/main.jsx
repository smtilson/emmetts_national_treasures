import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./useTailwind.css";
import { GlobalProvider } from "./contexts/baseContext.jsx";

import App from "./App.jsx";

document.documentElement.classList.add("dark");
createRoot(document.getElementById("root")).render(
  <StrictMode>
    <GlobalProvider>
      <App/>
    </GlobalProvider>
  </StrictMode>
);
