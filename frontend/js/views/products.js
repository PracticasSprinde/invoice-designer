// Funcion para inicializar la vista de productos
function initProducts() {

    // Boton abrir el formulario
    const btnNewProduct = document.querySelector(".new product");

    // Boton para cerrar el modal de productos
    const btnCloseModal = document.querySelector(".btn-close-modal");

    // Boton para cancelar el modal de productos
    const btnCancelModal = document.querySelector(".btn-cancel");

    // Modal de productos
    const modalProducts = document.querySelector(".modal-products");

    // Evento, abre formulario
    btnNewProduct.addEventListener("click", function () {
        modalProducts.style.display = "flex";
    });

    // Evento, cierra formulario
    btnCloseModal.addEventListener("click", function () {
        modalProducts.style.display = "none";
    });

    // Evento, cancela formulario
    btnCancelModal.addEventListener("click", function () {
        modalProducts.style.display = "none";
    });
}