import React from 'react';

type CardItem = {
  title: string;
  description?: string;
  imageUrl?: string;
  actionLabel?: string;
  actionUrl?: string;
};

type CarouselProps = {
  cards: CardItem[];
};

const CarouselComponent: React.FC<CarouselProps> = ({ cards }) => {
  return (
    <div className="overflow-x-auto flex space-x-4 p-2">
      {cards.map((card, index) => (
        <div
          key={index}
          className="min-w-[250px] bg-white rounded-lg shadow-md p-4 flex-shrink-0"
        >
          {card.imageUrl && (
            <img
              src={card.imageUrl}
              alt={card.title}
              className="w-full h-32 object-cover rounded-md mb-2"
            />
          )}
          <h3 className="text-lg font-semibold">{card.title}</h3>
          {card.description && (
            <p className="text-gray-700 text-sm mt-1">{card.description}</p>
          )}
          {card.actionLabel && card.actionUrl && (
            <a
              href={card.actionUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-3 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              {card.actionLabel}
            </a>
          )}
        </div>
      ))}
    </div>
  );
};

export default CarouselComponent;
