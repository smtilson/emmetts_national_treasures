import PropTypes from "prop-types";

export function TextInput({ styles, label, name, placeholder, id, required }) {
  return (
    <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
      <label htmlFor={id} className="whitespace-nowrap">
        {label}
      </label>
      <input
        type="text"
        name={name}
        id={id}
        placeholder={placeholder}
        required={required}
        className={styles}
      />
    </div>
  );
}

export function EmailInput({ styles, modifier }) {
  let mod = modifier || "";
  if (mod !== "") {
    mod = mod + "-";
  }
  return (
    <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
      <label htmlFor={mod + "email"} className="whitespace-nowrap">
        Email:
      </label>
      <input
        type="email"
        name={mod + "email"}
        id={mod + "email"}
        placeholder="Email"
        required
        className={styles}
      />
    </div>
  );
}

export function PasswordInput({ styles, modifier }) {
  let mod = modifier || "";
  if (mod !== "") {
    mod = mod + "-";
  }
  return (
    <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
      <label htmlFor={mod + "password"} className="whitespace-nowrap">
        Password:
      </label>
      <input
        type="password"
        name={mod + "password"}
        id={mod + "password"}
        placeholder="Password"
        required
        className={styles}
      />
    </div>
  );
}

export function ConfirmPasswordInput({ styles, modifier }) {
  let mod = modifier || "";
  if (mod !== "") {
    mod = mod + "-";
  }
  return (
    <div className="grid grid-cols-[1fr_2fr] gap-2 items-center mb-2">
      <label htmlFor="confirm-password" className="whitespace-nowrap">
        Password
      </label>
      <input
        type="password"
        name={mod + "confirm-password"}
        id={mod + "confirm-password"}
        placeholder="Confirm Password"
        required
        className={styles}
      />
    </div>
  );
}

TextInput.propTypes = {
  styles: PropTypes.string,
  label: PropTypes.string.isRequired,
  name: PropTypes.string.isRequired,
  placeholder: PropTypes.string,
  id: PropTypes.string.isRequired,
  required: PropTypes.bool.isRequired,
};

EmailInput.propTypes = {
  styles: PropTypes.string,
  modifier: PropTypes.string,
};

PasswordInput.propTypes = {
  styles: PropTypes.string,
  modifier: PropTypes.string,
};
ConfirmPasswordInput.propTypes = {
  styles: PropTypes.string,
  modifier: PropTypes.string,
};
