import Header from "./Header.jsx"
import Footer from "./Footer.jsx"
import Food from "./Food.jsx";

function App() {
  return (
    <>
      <Header />
      <Food foods={["random", "randome"]} />
      <Footer />
    </>
  );
}

export default App
