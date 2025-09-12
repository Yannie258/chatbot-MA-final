import React from 'react';
import { BookOpen, Users, MapPin, Calendar, GraduationCap, Building } from 'lucide-react';
import QuickLinks from './QuickLinks';
import ContactInfo from './ContactInfo';

const MainSessions = () => {
  return (
    <>
      {/* Hero Section */}
      <div className="px-4 py-16 bg-gray-50">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">Quick Access</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Everything you need to get started at TU Chemnitz. Click on any section to learn more.
          </p>
        </div>
        <QuickLinks />
      </div>

      {/* About Section */}
      <div className="px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-800 mb-8">About TU Chemnitz</h2>
          <div className="grid md:grid-cols-3 gap-8 mb-12">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl font-bold text-green-600 mb-2">11,000+</div>
              <p className="text-gray-600">Students</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl font-bold text-green-600 mb-2">8</div>
              <p className="text-gray-600">Faculties</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="text-3xl font-bold text-green-600 mb-2">1836</div>
              <p className="text-gray-600">Founded</p>
            </div>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">
            Technische Universität Chemnitz is a modern university with a strong focus on technology,
            natural sciences, economics, and humanities. Located in the heart of Saxony, we provide
            excellent education and research opportunities in a dynamic and innovative environment.
          </p>
        </div>
      </div>

      {/* Contact Section */}
      <div className="px-4 py-16 bg-gray-50">
        <ContactInfo />
      </div>
    </>
  );
};

export default MainSessions;
