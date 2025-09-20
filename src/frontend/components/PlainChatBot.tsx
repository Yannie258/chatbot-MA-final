'use client'

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import TypingIndicator from './TypingIndicator'
import { ContentType } from '@/enums/ContentType'

type TextMessage = {
    role: 'user' | 'bot'
    content_type: ContentType.TEXT
    content: string
    typing?: boolean
}

type Message = TextMessage

type Props = {
    apiUrl: string
}

export default function PlainChatBot({ apiUrl }: Props) {
    const [isChatbotOpen, setIsChatbotOpen] = useState(false)
    const [messages, setMessages] = useState<Message[]>([])
    const messagesEndRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
        }
    }, [messages])

    const handleSend = async (message: string) => {
        if (!message.trim()) return

        // user message
        setMessages(prev => [
            ...prev,
            { role: 'user', content_type: ContentType.TEXT, content: message },
        ])

        // typing indicator
        setMessages(prev => [
            ...prev,
            { role: 'bot', content_type: ContentType.TEXT, content: '', typing: true },
        ])

        try {
            const res = await fetch(`${apiUrl}/chatbot`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, strategy: 'plain' }),
            })

            const data = await res.json()
            console.log('RAW backend data:', data)

            // --- normalize content ---
            let content = data.content
            if (data.content_type === ContentType.TEXT && typeof content === 'string') {
                try {
                    if (content.startsWith('"') && content.endsWith('"')) {
                        content = JSON.parse(content) // unwrap JSON string
                    } else {
                        content = content.replace(/^"(.*)"$/, '$1')
                    }
                } catch (e) {
                    console.warn('Could not parse content, using raw:', content)
                }
            }

            // --- build normalized ---
            const normalized: Message = {
                role: 'bot',
                content_type: ContentType.TEXT,
                content: String(content),
            }

            setMessages(prev => [...prev.filter(m => !m.typing), normalized])
        } catch (error) {
            console.error('Error fetching response:', error)
            setMessages(prev => [
                ...prev.filter(m => !m.typing),
                {
                    role: 'bot',
                    content_type: ContentType.TEXT,
                    content: 'Error: could not connect.',
                },
            ])
        }
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {!isChatbotOpen ? (
                <button
                    className="bg-green-600 p-2 rounded-full shadow-lg hover:scale-105 transition"
                    onClick={() => {
                        setIsChatbotOpen(true)
                        setMessages(prev =>
                            prev.length === 0
                                ? [
                                    ...prev,
                                    {
                                        role: 'bot',
                                        content_type: ContentType.TEXT,
                                        content: 'Hello! How can I assist you today?',
                                    },
                                ]
                                : prev,
                        )
                    }}
                >
                    <Image src="/chat-icon.svg" alt="Chat Icon" width={45} height={45} />
                </button>
            ) : (
                <div className="w-96 h-150 bg-white rounded-xl shadow-2xl flex flex-col overflow-hidden">
                    <div className="bg-green-600 text-white px-4 py-2 font-bold flex justify-between items-center">
                        <span>TUCBot</span>
                        <button onClick={() => setIsChatbotOpen(false)}>✖</button>
                    </div>

                    {/* messages */}
                    <div className="flex-1 p-3 overflow-y-auto space-y-2 text-sm text-gray-800 text-left">
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`flex items-end ${msg.role === 'user' ? 'justify-end' : 'justify-start'
                                    }`}
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
                                    className={`relative px-3 py-2 rounded-lg text-sm ${msg.role === 'user'
                                            ? 'bg-green-500 text-white self-end max-w-[75%] user-tail'
                                            : 'bg-gray-100 text-gray-900 self-start max-w-[75%] bot-tail'
                                        }`}
                                >
                                    {msg.typing ? (
                                        <TypingIndicator />
                                    ) : (
                                        <div className="prose prose-sm max-w-full break-words whitespace-pre-wrap">
                                            <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                                {msg.content}
                                            </ReactMarkdown>
                                        </div>

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

                    {/* input */}
                    <form
                        className="border-t p-2 flex"
                        onSubmit={e => {
                            e.preventDefault()
                            const input = e.currentTarget.elements.namedItem(
                                'message',
                            ) as HTMLInputElement
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
