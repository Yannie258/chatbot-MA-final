import React from 'react';
import { Heart } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white px-4 py-12">
          <div className="max-w-6xl mx-auto grid md:grid-cols-4 gap-8">
            <div>
              <h4 className="font-bold mb-4 flex items-center">
                <Heart className="mr-2 text-green-400" size={20} />
                TU Chemnitz
              </h4>
              <p className="text-gray-300 text-sm">
                Excellence in education and research since 1836.
              </p>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Students</h5>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>Course Registration</li>
                <li>Student Portal</li>
                <li>Campus Life</li>
                <li>Support Services</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Academics</h5>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>Faculties</li>
                <li>Research</li>
                <li>Library</li>
                <li>International</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-4">Connect</h5>
              <ul className="space-y-2 text-sm text-gray-300">
                <li>Contact Us</li>
                <li>News & Events</li>
                <li>Social Media</li>
                <li>Alumni Network</li>
              </ul>
            </div>
          </div>
          <div className="max-w-6xl mx-auto mt-8 pt-8 border-t border-gray-700 text-center text-gray-400 text-sm">
            <p>&copy; 2024 Technische Universität Chemnitz. All rights reserved.</p>
          </div>
        </footer>
  );
};

export default Footer;
