import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";
import { useState } from "react";

type CarouselItem = {
  title: string;
  description: string;
  action_url?: string;
  action_label?: string;
};

type FollowUpOptions = {
  title: string;
  options: string[];
};

type CarouselProps = {
  type: ContentType.CAROUSEL;
  items: CarouselItem[];
  follow_up_options?: FollowUpOptions;
  onUserAction?: (choice: string) => void;
};

export default function CarouselComponent({ items, follow_up_options, onUserAction }: CarouselProps) {
  // Move useState outside the map - track expanded state for each item
  const [expandedItems, setExpandedItems] = useState<{ [key: number]: boolean }>({});

  const toggleExpanded = (index: number) => {
    setExpandedItems(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <div className="w-full">
      {/* Carousel Section */}
      <div className="overflow-x-auto pb-2">
        <div className="flex space-x-3 min-w-max px-2">
          {items.map((item, idx) => {
            const link = item.action_url ? normalizeUrl(item.action_url) : null;
            const expanded = expandedItems[idx] || false;
            
            return (
              <div
                key={idx}
                className="flex-shrink-0 w-[220px] bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <h4 className="font-semibold text-sm mb-2 text-gray-800">
                  {item.title}
                </h4>

                <p className="text-gray-600 text-xs mb-3">
                  {expanded ? item.description : item.description.slice(0, 80) + (item.description.length > 80 ? "..." : "")}
                  {item.description.length > 80 && (
                    <button
                      onClick={() => toggleExpanded(idx)}
                      className="ml-1 text-blue-600 hover:underline text-xs"
                    >
                      {expanded ? "Show less" : "Show more"}
                    </button>
                  )}
                </p>

                {/* Debug: Add console log to check if link exists */}
                {link && (
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-blue-600 hover:text-green-700 text-xs font-medium hover:underline"
                  >
                    {item.action_label || "Learn more"}
                  </a>
                )}
                
                {/* Debug: Show when no link is available */}
                {!link && item.action_url && (
                  <div className="text-red-500 text-xs">
                    Invalid URL: {item.action_url}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Follow-up Options Section */}
      {follow_up_options && (
        <div className="mt-4 pt-3 border-t border-gray-100">
          <h5 className="text-sm font-medium text-gray-700 mb-3">
            {follow_up_options.title}
          </h5>
          <div className="flex flex-wrap gap-2">
            {follow_up_options.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => onUserAction?.(option)}
                className="px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-medium rounded-md transition-colors"
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