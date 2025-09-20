import { ContentType } from "@/enums/ContentType";

type QuickReplyButtons = {
  type: ContentType.BUTTON;
  title?: string;
  description?: string;  // Changed from follow_up to match schema
  options: string[];
  onSelect: (value: string) => void;
};

export default function QuickReplyButtons({ title, description, options, onSelect }: QuickReplyButtons) {
  return (
    <div className="space-y-3">
      {(title || description) && (
        <div>
          {title && (
            <h4 className="font-semibold text-sm text-gray-800 mb-1">
              {title}
            </h4>
          )}
          {description && (
            <p className="text-xs text-gray-600">
              {description}
            </p>
          )}
        </div>
      )}

      <div className="grid grid-cols-1 gap-2">
        {options.map((opt, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(opt)}
            className="w-full text-center px-3 py-2 bg-green-50 hover:bg-green-500 border hover:text-white hover:border-green-700 rounded-md text-sm text-gray-700 hover:text-green-700 transition-colors font-medium"
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  );
}