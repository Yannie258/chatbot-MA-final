import React from 'react';
import { BookOpen, Users, MapPin, Calendar, GraduationCap, Building } from 'lucide-react';

const QuickLinks= () => {
    const links = [
        { icon: BookOpen, title: 'Course Registration', desc: 'Register for your courses and manage your schedule' },
        { icon: Users, title: 'Student Services', desc: 'Student support, counseling, and administrative help' },
        { icon: MapPin, title: 'Campus Map', desc: 'Find your way around the TU Chemnitz campus' },
        { icon: Calendar, title: 'Events & Activities', desc: 'Discover orientation events and student activities' },
        { icon: GraduationCap, title: 'Academic Resources', desc: 'Library, research facilities, and study support' },
        { icon: Building, title: 'Campus Facilities', desc: 'Dormitories, dining halls, and recreational facilities' }
      ];
    
      return (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {links.map((link, idx) => (
            <div key={idx} className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow border border-gray-100">
              <div className="flex items-center mb-4">
                <link.icon className="text-green-600 mr-3" size={24} />
                <h3 className="text-lg font-semibold text-gray-800">{link.title}</h3>
              </div>
              <p className="text-gray-600 text-sm">{link.desc}</p>
            </div>
          ))}
        </div>
      );
};

export default QuickLinks;