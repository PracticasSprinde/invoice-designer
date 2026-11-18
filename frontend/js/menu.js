// Funcion para cargar la vista seleccionada en el menú del sidebar
async function loadView(name) {
  const response = await fetch(`views/${name}.html`); //Solicita archivo HTML
  const html = await response.text();
  document.getElementById("view").innerHTML = html; // Busca elemento HTML con etiqueta "view"

  // Inicializar la vista de clientes
  if (name === "clients") {
    initClients();
  }

  // Inicializar la vista de productos
  if (name === "products") {
    initProducts();
  }

  // Inicializar la vista de facturas
  if (name === "invoices") {
    initInvoices();
  }

  // Inicializar la vista de emisor
  if (name === "issuer") {
    initIssuer();
  }

  // Inicializar la vista de plantillas
  if (name === "templates") {
    initTemplates();
  }

  // Inicializar la vista de editro
  if (name === "editor") {
    initEditor();
  }
}

// Detecta los clicks del menú
document.querySelectorAll("nav a").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    // Quitar la clase active de todos los enlaces
    document.querySelectorAll("nav a").forEach(function (item) {
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