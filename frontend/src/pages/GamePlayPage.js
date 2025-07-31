import React from 'react';
import { useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Gamepad2, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const GamePlayPage = () => {
  const { gameId } = useParams();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="p-6">
        <Link to="/games" className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Games
        </Link>
        
        <div className="max-w-4xl mx-auto">
          <div className="card">
            <div className="card-body text-center py-16">
              <Gamepad2 className="h-16 w-16 text-gray-400 mx-auto mb-6" />
              <h1 className="text-3xl font-bold text-gray-900 mb-4">Game #{gameId}</h1>
              <p className="text-lg text-gray-600 mb-8">
                This interactive game is designed to help discover your child's passions and talents.
              </p>
              <div className="bg-gray-100 rounded-lg p-8 mb-8">
                <p className="text-gray-700">
                  Game content and interactive elements will be implemented here.
                  This will include age-appropriate challenges, puzzles, and activities
                  that collect behavioral data for passion detection.
                </p>
              </div>
              <button className="btn btn-primary text-lg px-8 py-3">
                Start Game
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GamePlayPage; 