//src/utils/auth.js
// Simple authentication utility

export const getToken = () => localStorage.getItem("access_token");

export const isAuthenticated = () => {
  const token = getToken();
  return token !== null && token !== undefined && token !== "";
};

export const logout = () => {
  localStorage.removeItem("access_token");
};

