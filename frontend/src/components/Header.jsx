import { useGlobalContext } from "../contexts/baseContext";

function Header() {
  const { user, isAuthenticated } = useGlobalContext();
  return (
    <header>
      <h1>My React App</h1>
      <nav>
        <ul>
          <li>
            <a href="#">Home</a>
          </li>
          <li>
            <a href="#">About</a>
          </li>
          <li>
            <a href="#">Contact</a>
          </li>
        </ul>
      </nav>
      <hr></hr>

      {isAuthenticated && (
        <h1>Welcome {user.handle ? user.handle : user.email}</h1>
      )}
      {!isAuthenticated && <h1>Welcome to the app!</h1>}
    </header>
  );
}

export default Header;
