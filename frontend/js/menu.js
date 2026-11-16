// Menú lateral: detecta qué sección se pulsa y carga su vista en #view
// Controla la navegacion del sidebar
const viewTitles = {
  invoices: "Facturas",
  clients: "Clientes",
  products: "Productos",
  templates: "Plantillas",
};

async function loadView(name) {
  const response = await fetch(`views/${name}.html`);
  const html = await response.text();
  document.getElementById("view").textContent = html;
  document.getElementById("view-title").textContent = viewTitles[name];
}

document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();
    loadView(link.dataset.view);
  });
});

loadView("invoices");