import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

import { AuthProvider } from './contexts/AuthContext';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ChildrenPage from './pages/ChildrenPage';
import GamesPage from './pages/GamesPage';
import GamePlayPage from './pages/GamePlayPage';
import PassionsPage from './pages/PassionsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ProfilePage from './pages/ProfilePage';
import TalentAssessmentPage from './pages/TalentAssessmentPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <div className="App">
            <Toaster position="top-right" />
            <AnimatePresence mode="wait">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/dashboard" element={<Layout><DashboardPage /></Layout>} />
                <Route path="/children" element={<Layout><ChildrenPage /></Layout>} />
                <Route path="/games" element={<Layout><GamesPage /></Layout>} />
                <Route path="/game-play" element={<Layout><GamePlayPage /></Layout>} />
                <Route path="/passions" element={<Layout><PassionsPage /></Layout>} />
                <Route path="/analytics" element={<Layout><AnalyticsPage /></Layout>} />
                <Route path="/profile" element={<Layout><ProfilePage /></Layout>} />
                <Route path="/assessment" element={<Layout><TalentAssessmentPage /></Layout>} />
              </Routes>
            </AnimatePresence>
          </div>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App; 