type CarouselItem = {
    title: string;
    description: string;
    action_url?: string;
    action_label?: string;
  };
  
  type CarouselProps = {
    type: "carousel";
    items: CarouselItem[];
  };
  
  export default function CarouselComponent({ items }: CarouselProps) {
    return (
      <div className="flex overflow-x-auto space-x-4 p-2">
        {items.map((item, idx) => (
          <div
            key={idx}
            className="min-w-[200px] bg-white border rounded-lg p-3 shadow-sm"
          >
            <h4 className="font-bold text-md mb-1">{item.title}</h4>
            <p className="text-gray-600 text-sm mb-2">{item.description}</p>
            {item.action_url && (
              <a
                href={item.action_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline text-sm"
              >
                {item.action_label || "Learn more"}
              </a>
            )}
          </div>
        ))}
      </div>
    );
  }
  