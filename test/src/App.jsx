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
  const handleSelectItem = (item) => {
    console.log("handleSelectItem called. \nUser selected " + item);
  };
  return (
    <>
      <Header />
      <ListGroup
        items={["spaghetti", "randome"]}
        heading={"Food but not really"}
        onSelectItem={handleSelectItem}
      />
      <ListGroup items={items} heading={"Random item list"} />
      <Footer />
    </>
  );
}

export default App;
