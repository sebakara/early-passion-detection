import api from './auth';

// Children API functions
export const getChildren = async () => {
  const response = await api.get('/children');
  return response.data;
};

export const getChild = async (childId) => {
  const response = await api.get(`/children/${childId}`);
  return response.data;
};

export const createChild = async (childData) => {
  const response = await api.post('/children', childData);
  return response.data;
};

export const updateChild = async (childId, childData) => {
  const response = await api.put(`/children/${childId}`, childData);
  return response.data;
};

export const deleteChild = async (childId) => {
  const response = await api.delete(`/children/${childId}`);
  return response.data;
};

export const getChildSessions = async (childId) => {
  const response = await api.get(`/children/${childId}/sessions`);
  return response.data;
};

export const getChildPassions = async (childId) => {
  const response = await api.get(`/children/${childId}/passions`);
  return response.data;
}; 