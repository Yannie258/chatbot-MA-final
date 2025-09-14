import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";


type CardProps = {
  type: ContentType.CARD;
  title: string;
  description: string;
  items?: string[];
  action_url?: string;
  action_label?: string;
};

export default function CardComponent({ title, description, items, action_url, action_label }: CardProps) {
  const link = normalizeUrl(action_url);

  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm max-w-sm">
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p className="text-gray-700 mb-4">{description}</p>
      {items && items.length > 0 && (
        <ol className="list-decimal list-inside text-gray-700 mb-4">
          {items.map((step, idx) => (
            <li key={idx}>{step}</li>
          ))}
        </ol>
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
    </div>
  );
}
