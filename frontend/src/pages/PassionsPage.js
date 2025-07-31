import React from 'react';
import { motion } from 'framer-motion';
import { Heart, TrendingUp } from 'lucide-react';

const PassionsPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Passions & Talents</h1>
      </div>
      
      <div className="card">
        <div className="card-body text-center py-12">
          <Heart className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No passions detected yet</h3>
          <p className="text-gray-600 mb-6">
            Start playing games with your children to discover their natural talents and interests.
          </p>
          <button className="btn btn-primary">
            <TrendingUp className="h-4 w-4 mr-2" />
            Start Detection
          </button>
        </div>
      </div>
    </div>
  );
};

export default PassionsPage; 