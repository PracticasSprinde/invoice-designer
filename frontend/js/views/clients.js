// Funcion para inicializar la vista de clientes
function initClients() {

    // Boton abrir el formulario
    const btnNewClient = document.querySelector(".new-client");

    // Formulario de clientes
    const formClients = document.querySelector(".form-clients");

    // Evento al pulsar el boton
    btnNewClient.addEventListener("click", function () {
        formClients.style.display = "flex";
    });

}