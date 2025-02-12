import { MouseEvent, useState } from "react";

function ListGroup({ items, heading, onSelectItem }) {
  //let items = props.items;
  //let heading = props.heading;
  // this useState is an example of a hook. It tells react that there may be state that changes.
  // this setSelectedIndex function is an example of a hook. It just works!
  const [selectedIndex, setSelectedIndex] = useState(-1);
  // this function is an example of a callback function. It is passed to the onClick event of the list items.
  const handleClick = (e, item, index) => {
    console.log("User clicked on " + item);
    console.log("Event: ");
    console.log(e);
    setSelectedIndex(index);
    onSelectItem(item);
  };
  return (
    <>
      <h1>{heading}</h1>
      {items.length === 0 && <p>No items to display</p>}
      <ul className="list-group">
        {items.map((item, index) => (
          <li
            key={item}
            className={
              selectedIndex === index
                ? "list-group-item active"
                : "list-group-item"
            }
            onClick={(e) => handleClick(e, item, index)}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ListGroup;
