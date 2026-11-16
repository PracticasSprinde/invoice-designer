// Menú lateral: detecta qué sección se pulsa y carga su vista en #view
// Controla la navegacion del sidebar


// Objeto viewTitles, saber que título esta seleccionado
const viewTitles = {
  invoices: "Facturas",
  clients: "Clientes",
  products: "Productos",
  templates: "Plantillas",
  editor: "Editor",
  issuer: "Mis datos fiscales",
  settings: "Configuración",
};

// Funcion para cargar la vista seleccionada en ele menú del sidebar
async function loadView(name) {
  const response = await fetch(`views/${name}.html`); //Solicita archivo HTML
  const html = await response.text();
  document.getElementById("view").innerHTML = html; // Busca elemento HTML con etiqueta "view"
  document.getElementById("view-title").textContent = viewTitles[name]; // Busca elemento HTML con etiqueta "view -title"
}

// Detecta los clicks del menú
document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    // Quitar la clase active de todos los enlaces
    document.querySelectorAll("nav a").forEach(function(item) {
      item.classList.remove("active");
    });

    // Añadir active al enlace pulsado (en css es .active)
    link.classList.add("active");

    loadView(link.dataset.view);
  });
});

// Ejecuta la función
loadView("invoices");
document.querySelector('[data-view="invoices"]').classList.add("active"); // Deja seleccionado el primer item