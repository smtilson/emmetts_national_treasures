function Food(props) {
  let food1 = props.foods[0];
  let food2 = props.foods[1];
  return (
    <ul>
      <li>{food1}</li>
      <li>{food2.toUpperCase()}</li>
    </ul>
  );
}

export default Food;
