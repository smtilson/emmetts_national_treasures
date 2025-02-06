import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import Food from "./components/Food.jsx";
import ListGroup from "./components/ListGroup.jsx";

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
    <>
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
    </>
  );
}

export default App;
