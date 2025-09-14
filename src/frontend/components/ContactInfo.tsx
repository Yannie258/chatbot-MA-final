import React from 'react';
import { MapPin, Phone, Mail, Globe } from 'lucide-react';
interface ContactInfoProps {
    name: string;
    email: string;
    phone: string;
}

export default function ContactInfo() {
    return (
        <div className="bg-white rounded-lg shadow-md p-6 max-w-4xl mx-auto">
          <h3 className="text-2xl font-bold text-gray-800 mb-6 text-center">Contact Information</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <div className="flex items-center">
                <MapPin className="text-green-600 mr-3" size={20} />
                <div>
                  <p className="font-semibold text-gray-800">Address</p>
                  <p className="text-gray-600 text-sm">Straße der Nationen 62, 09111 Chemnitz, Germany</p>
                </div>
              </div>
              <div className="flex items-center">
                <Phone className="text-green-600 mr-3" size={20} />
                <div>
                  <p className="font-semibold text-gray-800">Phone</p>
                  <p className="text-gray-600 text-sm">+49 371 531-0</p>
                </div>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex items-center">
                <Mail className="text-green-600 mr-3" size={20} />
                <div>
                  <p className="font-semibold text-gray-800">Email</p>
                  <p className="text-gray-600 text-sm">info@tu-chemnitz.de</p>
                </div>
              </div>
              <div className="flex items-center">
                <Globe className="text-green-600 mr-3" size={20} />
                <div>
                  <p className="font-semibold text-gray-800">Website</p>
                  <p className="text-gray-600 text-sm">www.tu-chemnitz.de</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      );
};

