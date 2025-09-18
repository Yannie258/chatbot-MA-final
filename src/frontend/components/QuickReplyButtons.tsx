import { ContentType } from "@/enums/ContentType";

type QuickReplyButtons = {
  type: ContentType.BUTTON;
  title?: string;
  options: string[];
  onSelect: (value: string) => void;
  follow_up?: string;
};

export default function QuickReplyButtons({ title, options, onSelect, follow_up }: QuickReplyButtons) {
  return (
    <div className="p-2">
      {title && <h4 className="font-semibold mb-2">{title}</h4>}
      <div className="flex gap-2 flex-wrap">
        {options.map((opt, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(opt)}
            className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 text-sm"
          >
            {opt}
          </button>
        ))}
        {follow_up && (
              <p className="text-sm text-gray-500 mt-3 italic">
                {follow_up}
              </p>
            )}
      </div>
    </div>
  );
}
