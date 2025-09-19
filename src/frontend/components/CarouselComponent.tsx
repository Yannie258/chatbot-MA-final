import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";

type CarouselItem = {
  title: string;
  description: string;
  action_url?: string;
  action_label?: string;
};

type FollowUp = {
  title: string;
  options: string[];
};

type CarouselProps = {
  type: ContentType.CAROUSEL;
  items: CarouselItem[];
  follow_up?: FollowUp;
  onUserAction?: (choice: string) => void; 
};

export default function CarouselComponent({ items,follow_up, onUserAction }: CarouselProps) {
  return (
    <div className="flex overflow-x-auto space-x-4 p-2">
      {items.map((item, idx) => {
        const link = normalizeUrl(item.action_url);
        return (

          <div
            key={idx}
            className="min-w-[200px] bg-white border rounded-lg p-3 shadow-sm"
          >
            <h4 className="font-bold text-md mb-1">{item.title}</h4>
            <p className="text-gray-600 text-sm mb-2">{item.description}</p>
            {item.action_url && (
              <a
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline text-sm"
              >
                {item.action_label || "Learn more"}
              </a>
            )}
          </div>
        )
      })}
      {follow_up && (
        <div className="mt-3">
          <h5 className="text-sm font-semibold mb-2">You might know more about:</h5>
          <div className="flex flex-wrap gap-2">
            {follow_up.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => onUserAction?.(option)}
                className="px-3 py-1 bg-green-600 text-white text-sm rounded-md hover:bg-green-700 w-[150px] text-center"
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
