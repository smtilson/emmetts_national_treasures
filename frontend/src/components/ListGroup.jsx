// MouseEvent from react was imported but not used.
import { useState } from "react";
import PropTypes from 'prop-types';
import MyListItem from "./ListItem.jsx";
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
    <div className="mb-6">
      <h1 className="text-2xl font-bold mb-4 text-white">{heading}</h1>
      {items.length === 0 && <p className="text-gray-400">No items to display</p>}
      <ul>
        {items.map((item, index) => (
          <MyListItem
            key={item}
            text={item}
            isSelected={selectedIndex === index}
            onItemClick={(e) => handleClick(e, item, index)}
          />
          //</MyListItem>
        ))}
      </ul>
      </div>
    </>
  );
}

ListGroup.propTypes = {
  items: PropTypes.array.isRequired,
  heading: PropTypes.string.isRequired,
  onSelectItem: PropTypes.func.isRequired,
};

export default ListGroup;
