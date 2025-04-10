import Header from "./components/Header.jsx";
import Footer from "./components/Footer.jsx";
import ListGroup from "./components/ListGroup.jsx";
import LoginForm from "./components/auth/Login.jsx";
import SignUp from "./components/auth/SignUp.jsx";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { GlobalProvider} from "./contexts/baseContext";

function App() {
  return (
    <GlobalProvider>
      <Header />
      <SignUp />
      <LoginForm />
      <Footer />
    </GlobalProvider>
  );
}

function Counters() {
  let args = [{ init: 5 }, { init: 10, end: 15 }];
  return (
    <>
      <ProperCounter init="5" />
      <br />
      <ProperCounter init={10} end={15} />
      <br />
      <h2>Counters from for loop:</h2>
      <br />
      {loopThruCounters(args)}
      <br />
    </>
  );
}

function loopThruCounters(args) {
  let jsx = [];
  for (const item of args) {
    jsx.push(
      <>
        <ProperCounter init={item.init} end={item.end} />
        <br />
      </>
    );
  }
  return jsx;
}
function ProperCounter({ init, end }) {
  init = parseInt(init || 0);
  end = parseInt(end || 0);
  let [count, setCount] = useState(init);
  useEffect(() => {
    console.log("Effect called");
    var timer = setInterval(() => {
      setCount((count) => {
        if (end && count >= end) {
          console.log("entered if block");
          console.log("end: " + end);
          console.log("count: " + count);
          console.log(count >= end);
          clearInterval(timer);
          return count;
        }
        const newCount = count + 1;
        console.log("newCount: " + newCount);
        return newCount;
      });
    }, 1500);
    return () => {
      console.log("Effect cleanup function called.");
      return clearInterval(timer);
    };
  }, []);
  return (
    <>
      <span>Initial value of the counter is {init}.</span>
      {end && <br />}
      {end && <span>It will count until it reaches {end}.</span>}
      <br />
      <span>The count is currently {count}.</span>
    </>
  );
}

function App1() {
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
      <SignUp />
      <Login />

      <ListGroup
        items={["spaghetti", "random"]}
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

ProperCounter.propTypes = {
  init: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
  end: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
};

export default App;
