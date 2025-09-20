import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";

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
  return (
    <div className="w-full">
      {/* Carousel Section */}
      <div className="overflow-x-auto pb-2">
        <div className="flex space-x-3 min-w-max px-2">
          {items.map((item, idx) => {
            const link = item.action_url ? normalizeUrl(item.action_url) : null;

            return (
              <div
                key={idx}
                className="flex-shrink-0 w-[220px] bg-white border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <h4 className="font-semibold text-sm mb-2 text-gray-800 line-clamp-2">
                  {item.title}
                </h4>
                <p className="text-gray-600 text-xs mb-3 line-clamp-3">
                  {item.description}
                </p>

                {link && (
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-blue-600 hover:text-green-700 text-xs font-medium hover:underline"
                  >
                    {item.action_label || "Learn more"}
                    <svg
                      className="w-4 h-4 text-gray-400 group-hover:text-green-600 transition-colors"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                      />
                    </svg>
                  </a>
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