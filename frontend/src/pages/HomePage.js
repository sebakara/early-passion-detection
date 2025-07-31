import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Brain, 
  Heart, 
  Gamepad2, 
  BarChart3, 
  Shield, 
  Users,
  ArrowRight,
  Star,
  Play
} from 'lucide-react';

const HomePage = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI-Powered Detection',
      description: 'Advanced machine learning algorithms analyze behavioral patterns to identify your child\'s natural talents and interests.'
    },
    {
      icon: Gamepad2,
      title: 'Interactive Games',
      description: 'Engaging, age-appropriate games designed to collect meaningful data while children have fun and learn.'
    },
    {
      icon: Heart,
      title: 'Passion Discovery',
      description: 'Discover your child\'s unique passions across multiple domains including art, music, science, sports, and more.'
    },
    {
      icon: BarChart3,
      title: 'Progress Tracking',
      description: 'Monitor your child\'s development with detailed analytics and insights over time.'
    },
    {
      icon: Shield,
      title: 'Privacy First',
      description: 'COPPA-compliant with strict data protection measures to keep your child\'s information safe and secure.'
    },
    {
      icon: Users,
      title: 'Family Focused',
      description: 'Designed for families with features that help parents understand and support their child\'s development.'
    }
  ];

  const passionDomains = [
    { name: 'Art & Creativity', color: 'from-pink-500 to-purple-600', icon: '🎨' },
    { name: 'Music & Rhythm', color: 'from-blue-500 to-cyan-600', icon: '🎵' },
    { name: 'Science & Discovery', color: 'from-green-500 to-emerald-600', icon: '🔬' },
    { name: 'Sports & Movement', color: 'from-orange-500 to-red-600', icon: '⚽' },
    { name: 'Leadership & Social', color: 'from-purple-500 to-pink-600', icon: '👑' },
    { name: 'Language & Communication', color: 'from-indigo-500 to-blue-600', icon: '📚' },
    { name: 'Logic & Mathematics', color: 'from-yellow-500 to-orange-600', icon: '🧮' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Navigation */}
      <nav className="relative z-10 px-4 py-6 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl flex items-center justify-between">
          <div className="flex items-center">
            <Brain className="h-8 w-8 text-primary-600" />
            <span className="ml-2 text-xl font-bold text-gray-900">Passion Detection</span>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/login"
              className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              Sign In
            </Link>
            <Link
              to="/register"
              className="btn btn-primary"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative px-4 py-20 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Discover Your Child's
              <span className="text-gradient block"> Hidden Talents</span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-600 max-w-3xl mx-auto">
              Our AI-powered platform uses interactive games and behavioral analysis to identify your child's 
              natural passions and talents from an early age, helping you nurture their unique potential.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                to="/register"
                className="btn btn-primary text-lg px-8 py-3"
              >
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link
                to="/about"
                className="btn btn-outline text-lg px-8 py-3"
              >
                <Play className="mr-2 h-5 w-5" />
                Watch Demo
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Why Choose Passion Detection?
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Our comprehensive approach combines cutting-edge technology with child development expertise.
            </p>
          </div>
          <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="card p-6 hover:shadow-lg transition-shadow"
              >
                <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-500 text-white mb-4">
                  <feature.icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Passion Domains Section */}
      <section className="py-20 bg-gray-50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              Discover Multiple Passion Domains
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Our system identifies talents across seven key developmental areas.
            </p>
          </div>
          <div className="mt-16 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {passionDomains.map((domain, index) => (
              <motion.div
                key={domain.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="group relative overflow-hidden rounded-lg bg-white p-6 shadow-md hover:shadow-lg transition-all duration-300"
              >
                <div className={`absolute inset-0 bg-gradient-to-r ${domain.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`} />
                <div className="relative">
                  <div className="text-4xl mb-4">{domain.icon}</div>
                  <h3 className="text-lg font-semibold text-gray-900">{domain.name}</h3>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
              What Parents Say
            </h2>
          </div>
          <div className="mt-16 grid grid-cols-1 gap-8 lg:grid-cols-3">
            {[
              {
                name: 'Sarah Johnson',
                role: 'Parent of 7-year-old',
                content: 'Passion Detection helped us discover our daughter\'s love for music. She\'s now taking piano lessons and thriving!',
                rating: 5
              },
              {
                name: 'Michael Chen',
                role: 'Parent of 5-year-old',
                content: 'The games are so engaging that my son doesn\'t even realize he\'s learning. The insights are incredibly accurate.',
                rating: 5
              },
              {
                name: 'Emily Rodriguez',
                role: 'Parent of 9-year-old',
                content: 'We found out our child has a natural talent for problem-solving. The recommendations have been spot-on.',
                rating: 5
              }
            ].map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                className="card p-6"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                <div>
                  <p className="font-semibold text-gray-900">{testimonial.name}</p>
                  <p className="text-sm text-gray-500">{testimonial.role}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-600 to-secondary-600">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Ready to Discover Your Child's Passions?
          </h2>
          <p className="mt-4 text-lg text-primary-100">
            Join thousands of parents who are already helping their children thrive.
          </p>
          <div className="mt-8">
            <Link
              to="/register"
              className="btn bg-white text-primary-600 hover:bg-gray-100 text-lg px-8 py-3"
            >
              Start Your Free Trial
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center">
                <Brain className="h-8 w-8 text-primary-400" />
                <span className="ml-2 text-xl font-bold">Passion Detection</span>
              </div>
              <p className="mt-4 text-gray-400">
                Helping parents discover and nurture their children's natural talents.
              </p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Product</h3>
              <ul className="mt-4 space-y-2">
                <li><a href="#" className="text-gray-300 hover:text-white">Features</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Pricing</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Games</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Support</h3>
              <ul className="mt-4 space-y-2">
                <li><a href="#" className="text-gray-300 hover:text-white">Help Center</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Privacy Policy</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Terms of Service</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-gray-400 tracking-wider uppercase">Company</h3>
              <ul className="mt-4 space-y-2">
                <li><a href="#" className="text-gray-300 hover:text-white">About</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Contact</a></li>
                <li><a href="#" className="text-gray-300 hover:text-white">Careers</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 border-t border-gray-800 pt-8 text-center">
            <p className="text-gray-400">&copy; 2024 Passion Detection. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage; 