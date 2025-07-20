'use client'

import { useState } from 'react'
import Image from 'next/image'

type Message = {
  role: 'user' | 'bot';
  content_type: 'markdown' | 'card' | 'html' | 'text';
  content: string | any;
}


export default function Chatbot() {
 //const [isOpen, setIsOpen] = useState(false)
 const [isChatbotOpen, setIsChatbotOpen] = useState(false)
 const [messages, setMessages] = useState<Message[]>([])

 const handleSend = async (message: string) => {
  if (!message.trim()) return

  setMessages((prev) => [
    ...prev, 
    { role: 'user', content_type: 'text', content: message }
  ])
  
  // Call backend
  const res = await fetch('http://localhost:8000/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  const data = await res.json();

  // Append the bot's response
  setMessages((prev) => [...prev, data]);
}


  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isChatbotOpen ? (
       <button
       onClick={() => setIsChatbotOpen(true)}
       className="bg-blue-600 p-2 rounded-full shadow-lg hover:scale-105 transition"
     >
       <Image
         src="/chat-icon.png"
         alt="Chat Icon"
         width={40}
         height={40}
         className="rounded-full"
       />
     </button>
      ) : (
        <div className="w-80 h-96 bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-blue-600 text-white px-4 py-2 font-bold flex justify-between items-center">
            <span>TUCBot</span>
            <button onClick={() => setIsChatbotOpen(false)}>✖</button>
          </div>
          <div className="flex-1 p-3 overflow-y-auto space-y-2 text-sm text-gray-800">
            {messages.map((msg, idx) => (
              <div key={idx} className="bg-blue-100 p-2 rounded-md">
                {msg.content}
              </div>
            ))}
          </div>
          <form
            className="border-t p-2 flex"
            onSubmit={(e) => {
              e.preventDefault()
              const input = (e.currentTarget.elements.namedItem('message') as HTMLInputElement)
              handleSend(input.value)
              input.value = ''
            }}
          >
            <input
              type="text"
              name="message"
              className="flex-1 px-2 py-1 border rounded-md mr-2 text-sm"
              placeholder="Type a message..."
            />
            <button
              type="submit"
              className="bg-blue-600 text-white px-3 rounded-md text-sm hover:bg-blue-700"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
