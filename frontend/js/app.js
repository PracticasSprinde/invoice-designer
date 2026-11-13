//contiene la lógica y las funciones que hacen funcionar la aplicación.
const API_URL = "http://127.0.0.1:8000";

async function loadUsers() {
  const response = await fetch(`${API_URL}/clients/`);
  const data = await response.json();
  document.getElementById("output").textContent = JSON.stringify(data, null, 2);
}

document.getElementById("load-btn").addEventListener("click", loadUsers);