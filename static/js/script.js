function toggleMenu() {
  const menu = document.getElementById('menu');
  menu.classList.toggle('show');
}
// Seleccionar todos los checkboxes
  const selectAll = document.getElementById('select-all');
  const checkboxes = document.querySelectorAll('.select-row');

    selectAll.addEventListener('change', () => {
      checkboxes.forEach(checkbox => {
        checkbox.checked = selectAll.checked;
      });
    });


  // Espera a que todo el DOM cargue
  document.addEventListener('DOMContentLoaded', () => {
    const hokoTitle = document.querySelector('.logo-title');
    const menu = document.querySelector('.menu');

    // Solo en móviles: alternar visibilidad al hacer clic en "HOKO"
    hokoTitle.addEventListener('click', () => {
      menu.classList.toggle('show');
    });
  });

//codigo filtro 

// Código filtro

const toggleIcon = document.querySelector('.popover-toggle');
const popover = document.querySelector('.popover');

// Mostrar o ocultar el popover al hacer clic en el botón
toggleIcon.addEventListener('click', (e) => {
  e.stopPropagation(); // Evitar que el evento se propague
  popover.classList.toggle('active'); // Alternar la clase 'active' en el popover
});

// Cierra el popover si se hace clic fuera de él
document.addEventListener('click', (e) => {
  if (!popover.contains(e.target) && !toggleIcon.contains(e.target)) {
    popover.classList.remove('active'); // Remover la clase 'active' para ocultar el popover
  }
});




