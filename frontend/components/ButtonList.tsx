type ButtonListProps = {
  text: string;
  buttons: string[]; // now expecting array of strings
  onSelect: (value: string) => void;
};

const ButtonList: React.FC<ButtonListProps> = ({ text, buttons, onSelect }) => {
  return (
    <div className="mt-2 p-3 bg-white rounded-md shadow-sm border text-sm space-y-2">
      <p className="text-gray-800">{text}</p>
      <div className="flex flex-wrap gap-2 mt-2">
        {buttons.map((label, index) => (
          <button
            key={index}
            onClick={() => onSelect(label)}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ButtonList;
