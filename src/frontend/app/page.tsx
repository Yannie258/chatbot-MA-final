import ChatBot from '../components/ChatBot';
import Header from "@/components/Header";
import Footer from '@/components/Footer';
import MainSessions from '@/components/MainSessions';
import PlainChatBot from '@/components/PlainChatBot';


export default function Home() {
  const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL || ''
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col items-center justify-center text-center px-4">
        <Header />
        <MainSessions />
        <Footer />
         {/* <ChatBot apiUrl={apiUrl} />  */}
        <PlainChatBot apiUrl={apiUrl} /> 
      </div>
    </>
  );
}
