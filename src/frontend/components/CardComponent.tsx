import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";
import ReactMarkdown from "react-markdown";

type FollowUpOptions = {
  title: string;
  options: string[];
};

type CardProps = {
  type: ContentType.CARD;
  title: string;
  description: string;
  items?: string[];
  action_url?: string;
  action_label?: string;
  follow_up_options?: FollowUpOptions;
  onUserAction?: (choice: string) => void; // callback for button clicks
};

export default function CardComponent({ title, description, items, action_url, action_label, follow_up_options, onUserAction }: CardProps) {
  const link = normalizeUrl(action_url);

  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm max-w-sm">
      <h3 className="font-bold text-lg mb-2"><ReactMarkdown>{title}</ReactMarkdown></h3>
      <div className="mb-4"><ReactMarkdown>{description}</ReactMarkdown></div>
      {items && items.length > 0 && (
        <ReactMarkdown>
          {items.map((item) => `- ${item}`).join("\n")}
        </ReactMarkdown>
      )}
      {action_url && (
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block bg-green-600 text-white px-4 py-2 mt-2 rounded-md hover:bg-green-700 text-sm font-medium text-center whitespace-normal break-words"
        >
          {action_label || "Learn more"}
        </a>
      )}
      {follow_up_options && (
        <div className="pt-3 border-t border-gray-100">
          <h5 className="text-sm font-medium text-gray-700 mb-2">
            {follow_up_options.title}
          </h5>
          <div className="flex flex-wrap gap-2">
            {follow_up_options.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => onUserAction?.(option)}
                className="px-3 py-1.5 bg-gray-100 hover:bg-green-100 text-gray-700 hover:text-green-700 rounded-md text-sm font-medium transition-colors"
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
