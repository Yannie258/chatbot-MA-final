import { ContentType } from "@/enums/ContentType";
import { normalizeUrl } from "@/utils/utils";

type LinkItem = {
  label: string;
  url: string;
};

type LinkListProps = {
  type: ContentType.LINK;
  label?: string;
  links: LinkItem[];
  description?: string;
};

export default function LinkList({ label, links, description }: LinkListProps) {
  return (
    <div className="space-y-3">
      {label && <h4 className="font-semibold mb-2">{label}</h4>}

      <div>
        {links.map((link, idx) => (
          <div key={idx} className="mb-1">
            <a
              href={normalizeUrl(link.url)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-2 bg-gray-50 hover:bg-green-50 hover:underline rounded transition-colors group text-sm"
            >
              <span className="text-blue-600 group-hover:text-green-700 italic">
                {link.label}
              </span>
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
          </div>
        ))}
      </div>
      <p>{description}</p>
    </div>
  );
}
