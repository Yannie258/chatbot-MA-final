import React from 'react'

type Props = {
  options: string[];
  onSelect: (option: string) => void;
}

export default function QuickReplyButtons({ options, onSelect }: Props) {
  return (
    <div className="flex space-x-2 mt-2">
      {options.map((option, idx) => (
        <button
          key={idx}
          className="bg-gray-200 hover:bg-gray-300 text-sm px-3 py-1 rounded"
          onClick={() => onSelect(option)}
        >
          {option}
        </button>
      ))}
    </div>
  )
}
