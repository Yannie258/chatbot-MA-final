import ChatBot from '../components/ChatBot';
import Header from "@/components/Header";
import Footer from '@/components/Footer';
import MainSessions from '@/components/MainSessions';


export default function Home() {
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-white flex flex-col items-center justify-center text-center px-4">
        <Header />
        <MainSessions />
        <Footer />
        <ChatBot apiUrl="http://localhost:8000/chat/structured" />
      </div>
    </>
  );
}
