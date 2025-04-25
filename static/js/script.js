// Función para el menú lateral
function toggleMenu() {
  const menu = document.getElementById('menu');
  menu.classList.toggle('show');
}

// Selección múltiple
document.addEventListener('DOMContentLoaded', function() {
  // Seleccionar todos los checkboxes
  const selectAll = document.getElementById('select-all');
  if (selectAll) {
    selectAll.addEventListener('change', function() {
      const checkboxes = document.querySelectorAll('.select-row');
      checkboxes.forEach(checkbox => {
        checkbox.checked = this.checked;
      });
    });
  }

  // Búsqueda en tiempo real
  const searchInput = document.getElementById('search-input');
  const btnBuscar = document.getElementById('btn-buscar');
  
  if (searchInput && btnBuscar) {
    btnBuscar.addEventListener('click', function() {
      const searchTerm = searchInput.value.toLowerCase();
      const rows = document.querySelectorAll('#products-table tbody tr');
      
      rows.forEach(row => {
        const nombre = row.cells[2].textContent.toLowerCase();
        const referencia = row.cells[3].textContent.toLowerCase();
        if (nombre.includes(searchTerm) || referencia.includes(searchTerm)) {
          row.style.display = '';
        } else {
          row.style.display = 'none';
        }
      });
    });
  }

  // Importar productos
  const importDropdown = document.getElementById('import-dropdown');
  if (importDropdown) {
    importDropdown.addEventListener('change', function() {
      if (this.value) {
        // Aquí puedes agregar lógica para importar productos
        console.log('Producto seleccionado para importar:', this.value);
      }
    });
  }
});









// Array de productos (con la propiedad imagen agregada)
const productos = [
  { id: 1, name: "Cargador Doble Batería", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" },
  { id: 2, name: "Reloj SKMEI 1274", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" },
  { id: 3, name: "Reloj Curren 8442", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" }
];


// Resto del código JavaScript de ejemplo.js
function mostrarListaProductos() {
  const input = document.getElementById("busqueda-producto").value.toLowerCase();
  const contenedor = document.getElementById("contenedor-productos");
  const cuerpo = document.getElementById("cuerpo-tabla");
  
  cuerpo.innerHTML = '';
  
  if (input.trim() === "") {
    contenedor.style.display = "none";
    return;
  }
  
  const productosFiltrados = productos.filter(p => 
    p.name.toLowerCase().includes(input)
  );
  
  if (productosFiltrados.length === 0) {
    contenedor.style.display = "none";
    return;
  }
  
  contenedor.style.display = "block";
  
  productosFiltrados.forEach(producto => {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td><img src="${producto.imagen}" alt="${producto.name}" width="50" height="50" /></td>
      <td>${producto.name}</td>
      <td><input type="text" class="precio-producto" value="${producto.precio}" oninput="calcularFila(this)" /></td>
      <td><input type="number" class="cantidad-producto" value="1" min="1" oninput="calcularFila(this)" /></td>
      <td class="total-fila">0</td>
      <td><button type="button" onclick="eliminarFila(this)">Eliminar</button></td>
    `;
    cuerpo.appendChild(fila);
    calcularFila(fila.querySelector(".precio-producto"));
  });
}

function calcularFila(input) {
  const fila = input.closest("tr");
  const precio = parseFloat(fila.querySelector(".precio-producto").value) || 0;
  const cantidad = parseInt(fila.querySelector(".cantidad-producto").value) || 0;
  const total = precio * cantidad;
  fila.querySelector(".total-fila").textContent = total.toFixed(2);
  calcularTotalGeneral();
}

function calcularTotalGeneral() {
  const filas = document.querySelectorAll("#cuerpo-tabla tr");
  let total = 0;
  filas.forEach(fila => {
    total += parseFloat(fila.querySelector(".total-fila").textContent) || 0;
  });
  document.getElementById("precio-total").textContent = total.toFixed(2);
}

function eliminarFila(boton) {
  const fila = boton.closest("tr");
  fila.remove();
  calcularTotalGeneral();
}


