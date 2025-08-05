import api from './auth';

// Games API functions
export const getGames = async () => {
  const response = await api.get('/games');
  return response.data;
};

export const getGame = async (gameId) => {
  const response = await api.get(`/games/${gameId}`);
  return response.data;
};

export const createGame = async (gameData) => {
  const response = await api.post('/games', gameData);
  return response.data;
};

export const updateGame = async (gameId, gameData) => {
  const response = await api.put(`/games/${gameId}`, gameData);
  return response.data;
};

export const deleteGame = async (gameId) => {
  const response = await api.delete(`/games/${gameId}`);
  return response.data;
};

export const getGamesByCategory = async (category) => {
  const response = await api.get(`/games/category/${category}`);
  return response.data;
};

export const getGamesByAge = async (age) => {
  const response = await api.get(`/games/age/${age}`);
  return response.data;
}; 