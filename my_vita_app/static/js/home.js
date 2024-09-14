document.addEventListener('DOMContentLoaded', () => {
    const productos = document.querySelectorAll('.producto');

    productos.forEach(producto => {
        producto.addEventListener('mouseover', () => {
            producto.classList.add('hover');
        });

        producto.addEventListener('mouseout', () => {
            producto.classList.remove('hover');
        });
    });
});