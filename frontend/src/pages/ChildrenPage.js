import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Users, Plus, Edit, Trash2, Calendar, Heart, Brain } from 'lucide-react';
import { getChildren, createChild, deleteChild } from '../api/children';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const ChildrenPage = () => {
  const [children, setChildren] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const { isAuthenticated, token, user } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    date_of_birth: '',
    gender: '',
    initial_interests: '',
    favorite_colors: '',
    favorite_activities: '',
    learning_style: ''
  });

  // Helper function to calculate age from date of birth
  const calculateAge = (dateOfBirth) => {
    const birthDate = new Date(dateOfBirth);
    const today = new Date();
    const age = Math.floor((today - birthDate) / (365.25 * 24 * 60 * 60 * 1000));
    return age;
  };

  // Helper function to format date
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  useEffect(() => {
    console.log('ChildrenPage: Auth status:', { isAuthenticated, token: !!token, user });
    fetchChildren();
  }, [isAuthenticated, token]);

  const fetchChildren = async () => {
    try {
      setLoading(true);
      console.log('Fetching children with token:', !!token);
      const childrenData = await getChildren();
      setChildren(childrenData);
    } catch (error) {
      console.error('Error fetching children:', error);
      console.error('Error response:', error.response);
      toast.error('Failed to load children. Please make sure you are logged in.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate date of birth
    if (!formData.date_of_birth) {
      toast.error('Please select a date of birth');
      return;
    }
    
    const birthDate = new Date(formData.date_of_birth);
    const today = new Date();
    const age = Math.floor((today - birthDate) / (365.25 * 24 * 60 * 60 * 1000));
    
    if (age < 3 || age > 12) {
      toast.error('Child must be between 3 and 12 years old');
      return;
    }
    
    try {
      // Convert form data to match backend schema
      const childData = {
        first_name: formData.first_name,
        last_name: formData.last_name || null,
        date_of_birth: birthDate.toISOString(),
        gender: formData.gender || null,
        initial_interests: formData.initial_interests ? formData.initial_interests.split(',').map(s => s.trim()).filter(s => s) : null,
        favorite_colors: formData.favorite_colors ? formData.favorite_colors.split(',').map(s => s.trim()).filter(s => s) : null,
        favorite_activities: formData.favorite_activities ? formData.favorite_activities.split(',').map(s => s.trim()).filter(s => s) : null,
        learning_style: formData.learning_style || null
      };

      console.log('Sending child data:', childData);
      await createChild(childData);
      toast.success('Child added successfully!');
      setShowAddModal(false);
      setFormData({
        first_name: '',
        last_name: '',
        date_of_birth: '',
        gender: '',
        initial_interests: '',
        favorite_colors: '',
        favorite_activities: '',
        learning_style: ''
      });
      fetchChildren();
    } catch (error) {
      console.error('Error adding child:', error);
      toast.error('Failed to add child. Please check your input and try again.');
    }
  };

  const handleDelete = async (childId) => {
    if (window.confirm('Are you sure you want to delete this child?')) {
      try {
        await deleteChild(childId);
        toast.success('Child deleted successfully!');
        fetchChildren();
      } catch (error) {
        console.error('Error deleting child:', error);
        toast.error('Failed to delete child');
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-900">Children</h1>
        </div>
        <div className="card">
          <div className="card-body text-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading children...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Children</h1>
        <button 
          onClick={() => setShowAddModal(true)}
          className="btn btn-primary"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Child
        </button>
      </div>

      {children.length === 0 ? (
        <div className="card">
          <div className="card-body text-center py-12">
            <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No children added yet</h3>
            <p className="text-gray-600 mb-6">
              Add your children to start tracking their passions and talents.
            </p>
            <button 
              onClick={() => setShowAddModal(true)}
              className="btn btn-primary"
            >
              <Plus className="h-4 w-4 mr-2" />
              Add Your First Child
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {children.map((child) => (
            <motion.div
              key={child.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="card hover:shadow-lg transition-shadow"
            >
              <div className="card-body">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">
                      {child.first_name} {child.last_name}
                    </h3>
                    <div className="flex items-center text-sm text-gray-500 mb-2">
                      <Calendar className="h-4 w-4 mr-1" />
                      <span>{calculateAge(child.date_of_birth)} years old</span>
                      {child.gender && (
                        <>
                          <span className="mx-2">•</span>
                          <span className="capitalize">{child.gender}</span>
                        </>
                      )}
                    </div>
                    <div className="text-xs text-gray-400">
                      Born: {formatDate(child.date_of_birth)}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <button className="p-1 text-gray-400 hover:text-gray-600">
                      <Edit className="h-4 w-4" />
                    </button>
                    <button 
                      onClick={() => handleDelete(child.id)}
                      className="p-1 text-gray-400 hover:text-red-600"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                {child.initial_interests && child.initial_interests.length > 0 && (
                  <div className="mb-3">
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <Heart className="h-4 w-4 mr-1" />
                      <span className="font-medium">Interests:</span>
                    </div>
                    <p className="text-sm text-gray-600">{child.initial_interests.join(', ')}</p>
                  </div>
                )}

                {child.favorite_activities && child.favorite_activities.length > 0 && (
                  <div className="mb-4">
                    <div className="flex items-center text-sm text-gray-600 mb-1">
                      <Brain className="h-4 w-4 mr-1" />
                      <span className="font-medium">Favorite Activities:</span>
                    </div>
                    <p className="text-sm text-gray-600">{child.favorite_activities.join(', ')}</p>
                  </div>
                )}

                <div className="flex items-center justify-between pt-3 border-t border-gray-100">
                  <span className="text-sm text-gray-500">
                    Level: {child.current_level}
                  </span>
                  <button className="btn btn-primary btn-sm">
                    View Progress
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {/* Add Child Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white rounded-lg p-6 w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto"
          >
            <h2 className="text-xl font-bold text-gray-900 mb-4">Add New Child</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  First Name *
                </label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter child's first name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Enter child's last name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date of Birth *
                </label>
                <input
                  type="date"
                  name="date_of_birth"
                  value={formData.date_of_birth}
                  onChange={handleInputChange}
                  required
                  max={new Date().toISOString().split('T')[0]}
                  min={new Date(Date.now() - 12 * 365.25 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">Child must be between 3-12 years old</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Gender
                </label>
                <select
                  name="gender"
                  value={formData.gender}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Initial Interests
                </label>
                <textarea
                  name="initial_interests"
                  value={formData.initial_interests}
                  onChange={handleInputChange}
                  rows="2"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="What does your child enjoy doing?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Favorite Colors
                </label>
                <input
                  type="text"
                  name="favorite_colors"
                  value={formData.favorite_colors}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="e.g., blue, red, green"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Favorite Activities
                </label>
                <textarea
                  name="favorite_activities"
                  value={formData.favorite_activities}
                  onChange={handleInputChange}
                  rows="2"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="What activities does your child love?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Learning Style
                </label>
                <select
                  name="learning_style"
                  value={formData.learning_style}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="">Select learning style</option>
                  <option value="visual">Visual</option>
                  <option value="auditory">Auditory</option>
                  <option value="kinesthetic">Kinesthetic</option>
                  <option value="reading">Reading/Writing</option>
                </select>
              </div>

              <div className="flex items-center justify-end space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary"
                >
                  Add Child
                </button>
              </div>
            </form>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default ChildrenPage; 