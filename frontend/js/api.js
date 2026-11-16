// Dirección base de la API
const API_URL = "http://127.0.0.1:8000";

// Pide datos a la API (GET) y los devuelve
async function apiGet(path) {
  const response = await fetch(`${API_URL}${path}`);

  if (!response.json) {
    throw new Error(`Error ${response.status} al pedir ${path}`);
  }

  return await response.json();
}