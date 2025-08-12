import React from 'react';

type LinkItem = {
  label: string;
  url: string;
};

type LinkListProps = {
  links: LinkItem[];
};

const LinkList: React.FC<LinkListProps> = ({ links }) => {
  return (
    <ul className="list-disc pl-5 text-blue-700 mt-2">
      {links.map((link, index) => (
        <li key={index}>
          <a
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline"
          >
            {link.label}
          </a>
        </li>
      ))}
    </ul>
  );
};

export default LinkList;
