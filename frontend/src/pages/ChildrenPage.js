import React from 'react';
import { motion } from 'framer-motion';
import { Users, Plus } from 'lucide-react';

const ChildrenPage = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Children</h1>
        <button className="btn btn-primary">
          <Plus className="h-4 w-4 mr-2" />
          Add Child
        </button>
      </div>
      
      <div className="card">
        <div className="card-body text-center py-12">
          <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No children added yet</h3>
          <p className="text-gray-600 mb-6">
            Add your children to start tracking their passions and talents.
          </p>
          <button className="btn btn-primary">
            <Plus className="h-4 w-4 mr-2" />
            Add Your First Child
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChildrenPage; 