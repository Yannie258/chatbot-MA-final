'use client'

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import ReactMarkdown from 'react-markdown';
import TypingIndicator from './TypingIndicator';
import StructuredResponse from './StructuredResponse';
import { ContentType } from '@/enums/ContentType';
import remarkGfm from 'remark-gfm';

type TextMessage = {
  role: "user" | "bot";
  content_type: ContentType.TEXT;
  content: string;
  typing?: boolean;
};

type CardMessage = {
  role: "bot";
  content_type: ContentType.CARD;
  content: {
    type: ContentType.CARD;
    title: string;
    description: string;
    items?: string[];
    action_url: string;
    action_label?: string;
  };
  typing?: boolean;
};

type ButtonMessage = {
  role: "bot";
  content_type: ContentType.BUTTON;
  content: {
    type: ContentType.BUTTON;
    title?: string;
    options: string[];
  };
  typing?: boolean;
};

type CarouselMessage = {
  role: "bot";
  content_type: ContentType.CAROUSEL;
  content: {
    type: ContentType.CAROUSEL;
    items: {
      title: string;
      description: string;
      action_url?: string;
      action_label?: string;
    }[];
  };
  typing?: boolean;
};

type LinkMessage = {
  role: "bot";
  content_type: ContentType.LINK;
  content: {
    type: ContentType.LINK;
    label?: string;
    links: { label: string; url: string }[];
  };
  typing?: boolean;
};

// List message (pure checklist, different from card)
type ListMessage = {
  role: "bot";
  content_type: "list";
  content: {
    type: "list";
    title: string;
    items: string[];
  };
  typing?: boolean;
};

type Message = TextMessage | CardMessage | ButtonMessage | CarouselMessage | LinkMessage | ListMessage;

type Props = {
  apiUrl: string;
}

export default function Chatbot({ apiUrl }: Props) {
  const [isChatbotOpen, setIsChatbotOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const chatbotUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // Load saved strategy from localStorage on component mount
  useEffect(() => {
    const saved = localStorage.getItem("outputStrategy")
  }, [])

  // reference for the scrollable div
  const messagesEndRef = useRef<HTMLDivElement | null>(null)

  // scroll effect when messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])


  const handleSend = async (message: string) => {
    if (!message.trim()) return

    const history = messages
      .filter((m) => !m.typing)
      .map((m) => {
        if (m.role === "bot") {
          return {
            role: "assistant",
            content:
              m.content_type === ContentType.TEXT
                ? m.content                // keep plain text clean
                : JSON.stringify(m.content) // stringify only structured objects
          };
        }
        return { role: "user", content: m.content };
      });




    setMessages((prev) => [
      ...prev,
      { role: 'user', content_type: ContentType.TEXT, content: message }
    ])

    // Add temporary typing indicator
    setMessages((prev) => [
      ...prev,
      { role: "bot", content_type: ContentType.TEXT, content: "", typing: true }
    ]);

    try {
      const res = await fetch(`${chatbotUrl}/chatbot`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, strategy: "plain", history }),
      });

      // Append the bot's response simply
      //setMessages((prev) => [...prev, data]);

      const data = await res.json();
      console.log("RAW backend data:", data);

      // --- Fix goes here ---
      // unwrap quotes or JSON-encoded strings
      if (data.content_type === ContentType.TEXT && typeof data.content === "string") {
        try {
          if (data.content.startsWith('"') && data.content.endsWith('"')) {
            data.content = JSON.parse(data.content); // parse cleanly
          } else {
            data.content = data.content.replace(/^"(.*)"$/, "$1");
          }
        } catch (e) {
          console.warn("Could not parse content, using raw:", data.content);
        }
      }

      // --- Now build normalized ---
      let normalized: Message;
      if (data.content_type === ContentType.TEXT) {
        normalized = {
          role: "bot",
          content_type: ContentType.TEXT,
          content: data.content, // ✅ now cleaned
        };
      } else {
        normalized = {
          role: "bot",
          content_type: data.content_type,
          content: data.content,
        } as Message;
      }

      setMessages((prev) => [
        ...prev.filter((m) => !m.typing),
        normalized,
      ]);


    } catch (error) {
      console.error("Error fetching response:", error);
      // Replace typing with error
      setMessages((prev) => [
        ...prev.filter((m) => !m.typing),
        { role: "bot", content_type: ContentType.TEXT, content: "Error: could not connect." }
      ]);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {!isChatbotOpen ? (
        <button
          className="bg-green-600 p-2 rounded-full shadow-lg hover:scale-105 transition"
          onClick={() => {
            setIsChatbotOpen(true)
            // Add bot greeting only if no messages exist
            setMessages((prev) =>
              prev.length === 0
                ? [...prev, {
                  role: 'bot',
                  content_type: ContentType.TEXT,
                  content: "Hello! How can I assist you today?"
                }]
                : prev
            )
          }}

        >
          <Image
            src="/chat-icon.svg"
            alt="Chat Icon"
            width={45}
            height={45}
          />
        </button>
      ) : (
        <div className="w-96 h-150 bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden">
          <div className="bg-green-600 text-white px-4 py-2 font-bold flex justify-between items-center">
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
                  className={`relative px-3 py-2 rounded-lg text-sm ${msg.role === "user"
                    ? "bg-green-500 text-white self-end max-w-[75%] user-tail"
                    : "bg-gray-100 text-gray-900 self-start max-w-[75%] bot-tail"
                    }`}
                >


                  {msg.typing ? (
                    <TypingIndicator />
                  ) : msg.content_type === ContentType.TEXT ? (
                    <>
                      <div className="prose prose-sm max-w-none leading-relaxed space-y-3">
                        <ReactMarkdown>
                          {(() => {
                            if (typeof msg.content === "string") {
                              try {
                                // if it's a JSON string (with extra quotes), parse it
                                if (msg.content.startsWith('"') && msg.content.endsWith('"')) {
                                  return JSON.parse(msg.content);
                                }
                                return msg.content;
                              } catch {
                                return msg.content;
                              }
                            }
                            return JSON.stringify(msg.content, null, 2);
                          })()}
                        </ReactMarkdown>



                      </div>

                    </>

                  ) : (
                    <StructuredResponse
                      response={msg}
                      onUserAction={(choice) => handleSend(choice)}
                    />
                  )}

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
            <div ref={messagesEndRef} />
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
              className="bg-green-600 text-white px-3 rounded-md text-sm hover:bg-green-700"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </div>
  )
}
