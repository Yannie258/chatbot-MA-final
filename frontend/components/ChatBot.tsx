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
  const chatbotUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [outputFormat, setOutputFormat] = useState('plain');


  const handleSend = async (message: string) => {
    if (!message.trim()) return

    setMessages((prev) => [
      ...prev,
      { role: 'user', content_type: 'text', content: message }
    ])

    // Call backend
    const res = await fetch(`${chatbotUrl}/chatbot`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, strategy: outputFormat }),
    });

    const data = await res.json();

    // Append the bot's response
    setMessages((prev) => [...prev, data]);
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isChatbotOpen ? (
        <button
          className="bg-blue-600 p-2 rounded-full shadow-lg hover:scale-105 transition"
          onClick={() => {
            setIsChatbotOpen(true)
            // Add bot greeting only if no messages exist
            setMessages((prev) =>
              prev.length === 0
                ? [...prev, {
                  role: 'bot',
                  content_type: 'text',
                  content: "Hello! How can I assist you today?"
                }]
                : prev
            )
          }}

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
        <div className="w-96 h-150 bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-blue-600 text-white px-4 py-2 font-bold flex justify-between items-center">
            <span>TUCBot</span>
            <button onClick={() => setIsChatbotOpen(false)}>✖</button>
          </div>
          <div className="flex-1 p-3 overflow-y-auto space-y-2 text-sm text-gray-800 text-left">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex items-end ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.role === 'bot' && (
                  <Image
                    src="/bot-icon.png"
                    alt="Bot"
                    width={24}
                    height={24}
                    className="rounded-full mr-2"
                  />
                )}

                <div
                  className={`max-w-xs px-3 py-2 rounded-lg text-sm ${msg.role === 'user'
                    ? 'bg-blue-500 text-white self-end'
                    : 'bg-gray-100 text-gray-900 self-start'
                    }`}
                >
                  {msg.content}
                </div>

                {msg.role === 'user' && (
                  <Image
                    src="/user-icon.png"
                    alt="User"
                    width={24}
                    height={24}
                    className="rounded-full ml-2"
                  />
                )}
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
              type="button"
              onClick={() => setIsSettingsOpen(!isSettingsOpen)}
              className="px-2 text-blue-600 hover:text-blue-800"
              title="Settings"
            >
              ⚙️
            </button>
            <button
              type="submit"
              className="bg-blue-600 text-white px-3 rounded-md text-sm hover:bg-blue-700"
            >
              Send
            </button>
          </form>
          {isSettingsOpen && (
            <div className="absolute right-0 bottom-[48px] bg-white p-4 border rounded shadow-md w-84 z-50 text-sm">
              <h3 className="font-bold mb-3 text-gray-800">Output Format</h3>
              <div className="flex flex-wrap gap-2">
                {['plain', 'markdown', 'json', 'few-shot'].map((option) => (
                  <button
                    key={option}
                    onClick={() => setOutputFormat(option)}
                    className={`px-3 py-1 rounded-full border transition ${outputFormat === option
                        ? 'bg-blue-600 text-white border-blue-600'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>
          )}

        </div>
      )}
    </div>
  )
}
