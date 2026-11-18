// Funcion para inicializar la vista de clientes
function initClients() {

    // Boton abrir el formulario
    const btnNewClient = document.querySelector(".new-client");

    // Boton para cerrar el modal de clientes
    const btnCloseModal = document.querySelector(".btn-close-modal");

    // Boton para cancelar el modal de clientes
    const btnCancelModal = document.querySelector(".btn-cancel");

    // Modal de clientes
    const modalClients = document.querySelector(".modal-clients");

    // Evento, abre formulario
    btnNewClient.addEventListener("click", function () {
        modalClients.style.display = "flex";
    });

    // Evento, cierra formulario
    btnCloseModal.addEventListener("click", function(){
        modalClients.style.display = "none";

    });

    // Evento, cancela formulario
    btnCancelModal.addEventListener("click", function(){
        modalClients.style.display = "none";
    })
}