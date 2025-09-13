type LinkItem = {
  label: string;
  url: string;
};

type LinkListProps = {
  type: "link";
  label?: string;
  links: LinkItem[];
};

export default function LinkList({ label, links }: LinkListProps) {
  return (
    <div className="p-2">
      {label && <h4 className="font-semibold mb-2">{label}</h4>}
      <ul className="list-disc list-inside text-sm text-blue-600">
        {links.map((link, idx) => (
          <li key={idx}>
            <a href={link.url} target="_blank" rel="noopener noreferrer">
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
