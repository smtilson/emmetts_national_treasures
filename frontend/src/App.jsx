import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import ListGroup from "./components/ListGroup.jsx";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "./theme.js";

function App() {
  let items = [
    "An item",
    "A second item",
    "A third item",
    "A fourth item",
    "And a fifth one",
  ];
  const handleSelectItem = (index) => {
    // this function will not be able to handle the state of the object since it doesn't "have access" to it.
    console.log("handleSelectItem called."); // \nUser selected " + item);
    console.log("Index: " + index);
  };
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Header />
      <ListGroup
        items={["spaghetti", "randome"]}
        heading={"Food but not really"}
        onSelectItem={handleSelectItem}
      />
      <ListGroup
        items={items}
        heading={"Random item list"}
        onSelectItem={handleSelectItem}
      />
      <Footer />
    </ThemeProvider>
  );
}

export default App;
