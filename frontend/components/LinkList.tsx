import React from 'react';

type LinkItem = {
  label: string;
  url: string;
};

type LinkListProps = {
  text: string;
  links: LinkItem[];
};

const LinkList: React.FC<LinkListProps> = ({ text, links }) => {
  return (
    <div className="mt-2 p-3 bg-white rounded-md shadow-sm border text-sm space-y-2">
      <p className="text-gray-800">{text}</p>
      <ul className="list-disc list-inside space-y-1">
        {links.map((link, idx) => (
          <li key={idx}>
            <a
              href={link.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              {link.label}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default LinkList;
