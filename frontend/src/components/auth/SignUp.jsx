import {
  EmailInput,
  PasswordInput,
  ConfirmPasswordInput,
  TextInput,
} from "../forms/Inputs";
function SignUp() {
  let styles = "border-2 border-light-gray-300 m-4 rounded";
  return (
    <div>
      <h3>Sign Up</h3>
      <form action="" className="signup-form flex flex-col space-y-4">
        <EmailInput styles={styles} modifier={"signup"} />
        <TextInput
          styles={styles}
          label={"Handle:"}
          name={"handle"}
          placeholder={"Handle"}
          id={"handle"}
        />
        <PasswordInput styles={styles} modifier={"signup"} />
        <ConfirmPasswordInput styles={styles} modifier={"signup"} />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}

export default SignUp;
