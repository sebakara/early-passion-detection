import React, { useState, useEffect } from 'react';
import { Brain, Clock, CheckCircle, ArrowRight, Star, Users } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import toast from 'react-hot-toast';

const TalentAssessmentPage = () => {
  const { isAuthenticated, token } = useAuth();
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [assessmentComplete, setAssessmentComplete] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchChildren();
    }
  }, [isAuthenticated]);

  const fetchChildren = async () => {
    try {
      const response = await fetch('/api/v1/children', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const childrenData = await response.json();
        setChildren(childrenData);
      }
    } catch (error) {
      console.error('Error fetching children:', error);
    }
  };

  const startAssessment = async (childId) => {
    setLoading(true);
    try {
      const response = await fetch(`/api/v1/questions/assessment/${childId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const assessmentData = await response.json();
        setQuestions(assessmentData.questions);
        setSelectedChild(children.find(c => c.id === childId));
        setCurrentQuestionIndex(0);
        setAssessmentComplete(false);
      }
    } catch (error) {
      console.error('Error starting assessment:', error);
      toast.error('Failed to start assessment');
    } finally {
      setLoading(false);
    }
  };

  const submitResponse = async (answer) => {
    const currentQuestion = questions[currentQuestionIndex];
    
    try {
      await fetch('/api/v1/questions/response', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          child_id: selectedChild.id,
          question_id: currentQuestion.id,
          answer: answer
        })
      });

      if (currentQuestionIndex < questions.length - 1) {
        setCurrentQuestionIndex(currentQuestionIndex + 1);
      } else {
        await completeAssessment();
      }
    } catch (error) {
      console.error('Error submitting response:', error);
      toast.error('Failed to submit response');
    }
  };

  const completeAssessment = async () => {
    try {
      const response = await fetch(`/api/v1/questions/assessment/${selectedChild.id}/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setAssessmentComplete(true);
        toast.success('Assessment completed!');
      }
    } catch (error) {
      console.error('Error completing assessment:', error);
      toast.error('Failed to complete assessment');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Authentication Required</h2>
          <p className="text-gray-600">Please log in to access talent assessments.</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading assessment...</p>
        </div>
      </div>
    );
  }

  if (assessmentComplete) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto text-center">
            <CheckCircle className="h-16 w-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Assessment Complete!
            </h2>
            <p className="text-gray-600 mb-6">
              The assessment for {selectedChild.first_name} has been completed successfully.
            </p>
            <button
              onClick={() => {
                setAssessmentComplete(false);
                setSelectedChild(null);
              }}
              className="bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Start New Assessment
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (selectedChild && questions.length > 0) {
    const question = questions[currentQuestionIndex];
    
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900">
                Question {currentQuestionIndex + 1} of {questions.length}
              </h3>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
                />
              </div>
            </div>

            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              {question.question_text}
            </h2>

            {question.question_type === 'multiple_choice' && question.options && (
              <div className="space-y-3">
                {question.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => submitResponse(option)}
                    className="w-full p-4 text-left border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-colors"
                  >
                    {option}
                  </button>
                ))}
              </div>
            )}

            {question.question_type === 'rating' && (
              <div className="space-y-4">
                <p className="text-gray-600">Rate your interest level:</p>
                <div className="flex justify-center space-x-2">
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <button
                      key={rating}
                      onClick={() => submitResponse(rating.toString())}
                      className="p-3 rounded-full border-2 border-gray-200 hover:border-yellow-400 hover:bg-yellow-50 transition-colors"
                    >
                      <Star className="h-6 w-6 text-yellow-400" />
                    </button>
                  ))}
                </div>
                <div className="flex justify-between text-sm text-gray-500">
                  <span>Not interested</span>
                  <span>Very interested</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <Brain className="h-16 w-16 text-blue-600 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-4">
              Talent Assessment
            </h1>
            <p className="text-lg text-gray-600">
              Discover your child's natural talents and interests
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Select a Child for Assessment
            </h2>
            
            {children.length === 0 ? (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-600 mb-4">No children found. Please add a child first.</p>
                <button
                  onClick={() => window.location.href = '/children'}
                  className="bg-blue-600 text-white py-2 px-6 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Add Child
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {children.map((child) => (
                  <div
                    key={child.id}
                    className="border border-gray-200 rounded-lg p-6 hover:border-blue-300 hover:shadow-md transition-all cursor-pointer"
                    onClick={() => startAssessment(child.id)}
                  >
                    <div className="flex items-center mb-4">
                      <Users className="h-6 w-6 text-blue-600 mr-3" />
                      <div>
                        <h3 className="font-semibold text-gray-900">
                          {child.first_name} {child.last_name}
                        </h3>
                        <p className="text-sm text-gray-500">
                          Age: {Math.floor((new Date() - new Date(child.date_of_birth)) / (365.25 * 24 * 60 * 60 * 1000))}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center text-sm text-gray-600 mb-4">
                      <Clock className="h-4 w-4 mr-1" />
                      <span>~10-15 minutes</span>
                    </div>
                    
                    <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center">
                      Start Assessment
                      <ArrowRight className="h-4 w-4 ml-2" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TalentAssessmentPage; 