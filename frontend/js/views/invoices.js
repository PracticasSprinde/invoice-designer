// Funcion para inicializar la vista de facturas
function initInvoices() {

    // Boton abrir el formulario
    const btnNewInvoice = document.querySelector(".new-invoice");

    // Boton para cerrar el modal de facturas
    const btnCloseModal = document.querySelector(".btn-close-modal");

    // Boton para cancelar el modal de facturas
    const btnCancelModal = document.querySelector(".btn-cancel");

    // Modal de facturas
    const modalInvoices = document.querySelector(".modal-invoices");

    // Evento, abre formulario
    btnNewInvoice.addEventListener("click", function () {
        modalInvoices.style.display = "flex";
    });

    // Evento, cierra formulario
    btnCloseModal.addEventListener("click", function() {
        modalInvoices.style.display = "none";

    });

    // Evento, cancela formulario
    btnCancelModal.addEventListener("click", function() {
        modalInvoices.style.display = "none";
    })
}