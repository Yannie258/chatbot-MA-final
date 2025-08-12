import React from 'react';

type CardProps = {
  title: string;
  description?: string;
  imageUrl?: string;
  actionLabel?: string;
  actionUrl?: string;
};

const CardComponent: React.FC<CardProps> = ({ title, description, imageUrl, actionLabel, actionUrl }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 mb-3">
      {imageUrl && (
        <img
          src={imageUrl}
          alt={title}
          className="w-full h-40 object-cover rounded-md mb-2"
        />
      )}
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && <p className="text-gray-700 text-sm mt-1">{description}</p>}
      {actionLabel && actionUrl && (
        <a
          href={actionUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-3 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
        >
          {actionLabel}
        </a>
      )}
    </div>
  );
};

export default CardComponent;
