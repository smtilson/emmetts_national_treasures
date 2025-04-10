import Input from "./Input.jsx";
import {PropTypes} from 'prop-types';
function Form({inputs, styles, onSubmit}) {
    return (
        <div>
            <form action="" onSubmit={onSubmit}>
                {inputs.map((input) => (
                    <Input key={input} />
                ))}
                <button type="submit" className={styles.button}>Submit</button>
            </form>
        </div>
    );
}

Form.propTypes = {
    inputs: PropTypes.array.isRequired,
    styles: PropTypes.object.isRequired,
    onSubmit: PropTypes.func.isRequired,
}
export default Form;