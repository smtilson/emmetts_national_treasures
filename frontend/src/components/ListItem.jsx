import PropTypes from 'prop-types';

function MyListItem({ text, isSelected, onItemClick }) {
    return (
        <li // was included in the classes 
            // border-transparent       /* Hide border initially */
            className={`
                rounded-lg                /* Rounded corners */
                p-4                      /* Padding */
                mb-2                     /* Spacing between items */
                border-2                 /* Border width (transparent by default) */
                transition-all           /* Smooth transitions */
                duration-420             /* Transition speed */
                !hover:bg-gray-700        /* Lighten background on hover */
                !active:border-gray-500       /* Show white border while clicking */
                cursor-pointer           /* Show pointer cursor */
                text-gray-300             /* Text color */
                ${isSelected 
                    ? 'bg-blue-900 border-blue-400' 
                    : 'bg-gray-800 hover:bg-gray-700 hover:border-gray-500'}

            `}
            onClick={onItemClick}
        >
        {text}
        </li>
        );
}

MyListItem.propTypes = {
  text: PropTypes.string,
  isSelected: PropTypes.bool,
  onItemClick: PropTypes.func,
};


MyListItem.defaultProps = {
    isSelected: false
  };

export default MyListItem;