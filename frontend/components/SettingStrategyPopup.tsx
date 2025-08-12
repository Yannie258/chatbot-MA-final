'use client';

import React, { useState } from 'react';

type SettingStrategyPopupProps = {
  selected: string;
  onChange: (value: string) => void; // Called when the user confirms/save their choice
  onClose: () => void; // Called when the popup is closed
};

const strategies = [
  { value: 'plain', label: 'Simple Text' },
  { value: 'markdown', label: 'Formatted Text' },
  { value: 'json', label: 'Structured Data' },
  { value: 'fewshot', label: 'Example-based Response' },
  { value: 'card', label: 'Information Card' },
  { value: 'carousel', label: 'Scrollable Cards' },
  { value: 'button', label: 'Interactive Buttons' },
  { value: 'link', label: 'List of Links' },
];

const SettingStrategyPopup: React.FC<SettingStrategyPopupProps> = ({
  selected,
  onChange,
  onClose,
}) => {
   // Set default strategy as Simple Text (value: 'plain')
   const [tempSelected, setTempSelected] = useState(selected || 'plain'); // Default to 'plain' if no selection is passed

  const handleSave = () => {
    onChange(tempSelected); // Save the selected value
    onClose(); // Close the popup
  };

  return (
    <div className="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-lg w-96 p-6">
        <h3 className="text-lg font-semibold mb-4">Select a Strategy</h3>
        <ul className="space-y-2">
          {strategies.map((strategy) => (
            <li
              key={strategy.value}
              className={`p-2 rounded-md cursor-pointer ${
                strategy.value === tempSelected
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 hover:bg-gray-200'
              }`}
              onClick={() => setTempSelected(strategy.value)} // Update temporary selection
            >
              {strategy.label}
            </li>
          ))}
        </ul>
        <div className="flex justify-end space-x-2 mt-4">
          <button
            className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
            onClick={onClose}
          >
            Cancel
          </button>
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            onClick={handleSave}
          >
            Save
          </button>
        </div>
      </div>
    </div>
  );
};

export default SettingStrategyPopup;