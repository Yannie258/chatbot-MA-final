import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";
import ReactMarkdown from "react-markdown";


type CardProps = {
  type: ContentType.CARD;
  title: string;
  description: string;
  items?: string[];
  action_url?: string;
  action_label?: string;
  follow_up_options?: string[];
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
      <p className="py-3">
        You can get more information about:
      </p>
      {follow_up_options && follow_up_options.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {follow_up_options.map((opt, idx) => (
            <button
              key={idx}
              className="w-48 bg-gray-500 text-white px-3 py-1 rounded-md text-sm hover:bg-green-600"
              onClick={() => onUserAction?.(opt)}
            >
              {opt}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
