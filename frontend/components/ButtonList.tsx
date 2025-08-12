import React from 'react';

type ButtonItem = {
  label: string;
  url: string;
};

type ButtonListProps = {
  buttons: ButtonItem[];
};

const ButtonList: React.FC<ButtonListProps> = ({ buttons }) => {
  return (
    <div className="flex flex-wrap gap-2 mt-2">
      {buttons.map((btn, index) => (
        <a
          key={index}
          href={btn.url}
          target="_blank"
          rel="noopener noreferrer"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
        >
          {btn.label}
        </a>
      ))}
    </div>
  );
};

export default ButtonList;
