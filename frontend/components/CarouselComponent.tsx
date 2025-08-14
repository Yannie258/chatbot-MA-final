import React from 'react';
import Image from 'next/image'

type CardItem = {
    title: string;
    description: string;
    image_url?: string;
    url?: string;
};

type CarouselProps = {
    cards: CardItem[];
};

const CarouselComponent: React.FC<CarouselProps> = ({ cards }) => {
    return (
        <div className="overflow-x-auto flex gap-4 p-2">
            {cards.map((card, index) => (
                <a
                    key={index}
                    href={card.url || '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="min-w-[250px] max-w-[250px] bg-white border rounded-lg shadow hover:shadow-lg transition duration-200"
                >
                    {card.image_url && (
                        <img
                            src={card.image_url}
                            alt={card.title}
                            width={250}
                            height={140}
                            className="rounded-t-lg object-cover"
                        />
                    )}
                    <div className="p-3">
                        <h3 className="text-md font-bold">{card.title}</h3>
                        <p className="text-sm text-gray-700 mt-1">{card.description}</p>
                    </div>
                </a>
            ))}
        </div>
    );
};

export default CarouselComponent;
