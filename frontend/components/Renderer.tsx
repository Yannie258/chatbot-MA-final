import React from 'react'
import ReactMarkdown from 'react-markdown'
import DOMPurify from 'dompurify'
import CardComponent from './CardComponent'
import QuickReplyButtons from './QuickReplyButtons'

type Message = {
  role: 'user' | 'bot';
  content_type: 'text' | 'markdown' | 'card' | 'html';
  content: string | any;
}

export default function Renderer({ message }: { message: Message }) {
  if (message.role === 'user') {
    return (
      <div className="bg-blue-100 p-2 rounded-md self-end">
        {message.content}
      </div>
    )
  }

  switch (message.content_type) {
    case 'markdown':
      return <ReactMarkdown>{message.content}</ReactMarkdown>

    case 'card':
      return <CardComponent {...message.content} />

    case 'html':
      return (
        <div
          dangerouslySetInnerHTML={{
            __html: DOMPurify.sanitize(message.content),
          }}
        />
      )

    default:
      return (
        <div className="bg-gray-100 p-2 rounded-md">
          {message.content}
        </div>
      )
  }
}
