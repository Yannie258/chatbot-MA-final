import Image from "next/image";
import Head from 'next/head'; 
import ChatBot from '@/components/ChatBot'

export default function Home() {
  return (
    <>
      <Head>
        <title>Student Onboarding Chatbot</title>
      </Head>
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col items-center justify-center text-center px-4">
        <h1 className="text-4xl font-bold mb-4 text-blue-800">Welcome to TU Student Hub</h1>
        <p className="text-lg text-gray-700 max-w-xl mb-8">
          Get guidance, ask questions, and explore your first week at the university — powered by AI.
        </p>
        <p className="text-sm text-gray-400">Scroll or chat with us anytime!</p>

        <ChatBot />
      </main>
    </>
  );
}
