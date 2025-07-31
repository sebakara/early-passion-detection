import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Users, 
  Gamepad2, 
  Heart, 
  BarChart3, 
  Plus,
  TrendingUp,
  Clock,
  Star
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const DashboardPage = () => {
  const { user } = useAuth();

  // Mock data - in real app, this would come from API
  const stats = [
    {
      name: 'Children',
      value: '2',
      icon: Users,
      color: 'bg-blue-500',
      href: '/children'
    },
    {
      name: 'Games Played',
      value: '15',
      icon: Gamepad2,
      color: 'bg-green-500',
      href: '/games'
    },
    {
      name: 'Passions Detected',
      value: '4',
      icon: Heart,
      color: 'bg-pink-500',
      href: '/passions'
    },
    {
      name: 'Total Play Time',
      value: '8.5h',
      icon: Clock,
      color: 'bg-purple-500',
      href: '/analytics'
    }
  ];

  const recentActivities = [
    {
      id: 1,
      child: 'Emma',
      activity: 'Completed Music Rhythm Game',
      time: '2 hours ago',
      type: 'game'
    },
    {
      id: 2,
      child: 'Emma',
      activity: 'New passion detected: Art & Creativity',
      time: '1 day ago',
      type: 'passion'
    },
    {
      id: 3,
      child: 'Liam',
      activity: 'Started Science Discovery Game',
      time: '2 days ago',
      type: 'game'
    },
    {
      id: 4,
      child: 'Liam',
      activity: 'Completed Logic Puzzle Game',
      time: '3 days ago',
      type: 'game'
    }
  ];

  const quickActions = [
    {
      name: 'Add Child',
      description: 'Create a new child profile',
      icon: Plus,
      href: '/children',
      color: 'bg-blue-500 hover:bg-blue-600'
    },
    {
      name: 'Start Game',
      description: 'Begin a new game session',
      icon: Gamepad2,
      href: '/games',
      color: 'bg-green-500 hover:bg-green-600'
    },
    {
      name: 'View Passions',
      description: 'Check passion analysis',
      icon: Heart,
      href: '/passions',
      color: 'bg-pink-500 hover:bg-pink-600'
    },
    {
      name: 'Analytics',
      description: 'View detailed reports',
      icon: BarChart3,
      href: '/analytics',
      color: 'bg-purple-500 hover:bg-purple-600'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg p-6 text-white">
        <h1 className="text-2xl font-bold">
          Welcome back, {user?.full_name || 'Parent'}! 👋
        </h1>
        <p className="mt-2 text-primary-100">
          Ready to discover more about your children's passions today?
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className="card p-6 hover:shadow-lg transition-shadow"
          >
            <Link to={stat.href} className="block">
              <div className="flex items-center">
                <div className={`flex-shrink-0 ${stat.color} rounded-md p-3`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                  <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
              </div>
            </Link>
          </motion.div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">Quick Actions</h2>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {quickActions.map((action, index) => (
              <motion.div
                key={action.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
              >
                <Link
                  to={action.href}
                  className="block p-4 border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-md transition-all"
                >
                  <div className={`inline-flex p-3 rounded-lg ${action.color} text-white mb-3`}>
                    <action.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-lg font-medium text-gray-900 mb-1">{action.name}</h3>
                  <p className="text-sm text-gray-600">{action.description}</p>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <div className="card-header">
          <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
        </div>
        <div className="card-body">
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg"
              >
                <div className="flex-shrink-0">
                  {activity.type === 'game' ? (
                    <Gamepad2 className="h-6 w-6 text-green-500" />
                  ) : (
                    <Heart className="h-6 w-6 text-pink-500" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900">
                    {activity.activity}
                  </p>
                  <p className="text-sm text-gray-500">
                    {activity.child} • {activity.time}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Tips Section */}
      <div className="card bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-200">
        <div className="card-body">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <Star className="h-6 w-6 text-yellow-500" />
            </div>
            <div className="ml-3">
              <h3 className="text-lg font-medium text-gray-900">Pro Tip</h3>
              <p className="mt-1 text-sm text-gray-600">
                Regular game sessions help our AI better understand your child's interests. 
                Try to have your children play at least 2-3 games per week for the most accurate passion detection.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage; 