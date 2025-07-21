import React from 'react'

type Props = {
  title: string;
  content: string;
  actions: string[];
}

export default function CardComponent({ title, content, actions }: Props) {
  return (
    <div className="border p-3 rounded-md shadow bg-white">
      <h3 className="font-bold text-blue-600">{title}</h3>
      <p className="text-sm mt-1">{content}</p>
      <div className="mt-2 flex space-x-2">
        {actions.map((action, idx) => (
          <button
            key={idx}
            className="text-xs bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600 transition"
            onClick={() => alert(`Clicked: ${action}`)}
          >
            {action}
          </button>
        ))}
      </div>
    </div>
  )
}
