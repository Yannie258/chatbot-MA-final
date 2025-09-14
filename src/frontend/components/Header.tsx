import React from 'react';
import { GraduationCap } from 'lucide-react';

const Header = () => {
    return (
        <div className="flex flex-col items-center justify-center text-center px-4 py-16">
          <div className="mb-8">
            <div className="w-20 h-20 bg-green-600 rounded-full flex items-center justify-center mb-4 mx-auto">
              <GraduationCap className="text-white" size={32} />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gray-800">
              Welcome to <span className="text-green-600">TU Chemnitz</span>
            </h1>
            <p className="text-lg text-gray-700 max-w-2xl mb-8">
              Herzlich willkommen! Get guidance, ask questions, and explore your first week at 
              Technische Universität Chemnitz — powered by AI assistance.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
                Start Your Journey
              </button>
              <button className="border border-green-600 text-green-600 hover:bg-green-50 px-8 py-3 rounded-lg font-semibold transition-colors">
                Campus Virtual Tour
              </button>
            </div>
          </div>
        </div>
    );
};

export default Header;