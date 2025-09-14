import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";


type CardProps = {
  type: ContentType.CARD;
  title: string;
  description: string;
  action_url?: string;
  action_label?: string;
};

export default function CardComponent({ title, description, action_url, action_label }: CardProps) {
  const link = normalizeUrl(action_url);
  
  return (
    <div className="bg-white border rounded-lg p-4 shadow-sm max-w-sm">
      <h3 className="font-bold text-lg mb-2">{title}</h3>
      <p className="text-gray-700 mb-4">{description}</p>
      {action_url && (
        <a
          href={action_url}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm"
        >
          {action_label || "Learn more"}
        </a>
      )}
    </div>
  );
}
