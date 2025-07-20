import React from 'react'
import ReactMarkdown from 'react-markdown'
import DOMPurify from 'dompurify'
import { ContentType } from './ContentType'
import CardComponent from './CardComponent'

export default function Renderer({ message }: { message: Message }) {
  if (message.role === 'user') {
    return (
      <div className="bg-blue-100 p-2 rounded-md self-end">
        {message.content}
      </div>
    )
  }

  switch (message.content_type) {
    case ContentType.Markdown:
      return <ReactMarkdown>{message.content}</ReactMarkdown>
    case ContentType.Card:
      return <CardComponent {...message.content} />
    case ContentType.Html:
      return (
        <div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(message.content) }} />
      )
    default:
      return <div className="bg-gray-100 p-2 rounded-md">{message.content}</div>
  }
}
