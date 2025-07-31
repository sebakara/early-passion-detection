import React from 'react';
import { motion } from 'framer-motion';
import { User, Settings } from 'lucide-react';

const ProfilePage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Profile</h1>
      </div>
      
      <div className="card">
        <div className="card-body text-center py-12">
          <User className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Profile settings</h3>
          <p className="text-gray-600 mb-6">
            Manage your account settings and preferences.
          </p>
          <button className="btn btn-primary">
            <Settings className="h-4 w-4 mr-2" />
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage; 