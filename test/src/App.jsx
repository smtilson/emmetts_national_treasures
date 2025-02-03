import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import Food from "./components/Food.jsx";
import ListGroup from "./components/ListGroup.jsx";

function App() {
  return (
    <>
      <Header />
      <Food foods={["random", "randome"]} />
      <ListGroup />
      <Footer />
    </>
  );
}

export default App;
