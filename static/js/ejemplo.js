
  // Array de productos (con la propiedad imagen agregada)
  const productos = [
    { id: 1, name: "Cargador Doble Batería", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" },
    { id: 2, name: "Reloj SKMEI 1274", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" },
    { id: 3, name: "Reloj Curren 8442", precio: 0.00, imagen: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTga9vIvcdH5UgOD5dRtHpEzBdh02UFsJzAkg&s" }
  ];
  

  // Función para mostrar u ocultar la lista de productos y agregarla a la tabla
  function mostrarListaProductos() {
    const input = document.getElementById("busqueda-producto").value.toLowerCase();
    const contenedor = document.getElementById("contenedor-productos");
    const cuerpo = document.getElementById("cuerpo-tabla");

    // Buscar el producto en la lista
    const producto = productos.find(p => p.name.toLowerCase().includes(input));

    // Si no se encuentra producto o el campo está vacío, ocultar la lista
    if (!producto || input.trim() === "") {
      contenedor.style.display = "none";
      return;
    }

    // Mostrar la lista de productos
    contenedor.style.display = "block";

    // Verificar si el producto ya está en la tabla
    const yaExiste = Array.from(cuerpo.rows).some(row => row.cells[0].textContent === producto.name);
    if (yaExiste) return; // No agregar si ya existe

    // Crear una nueva fila con el producto encontrado
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
  }

  // Función para calcular el total de una fila
  function calcularFila(input) {
    const fila = input.closest("tr");
    const precio = parseFloat(fila.querySelector(".precio-producto").value) || 0;
    const cantidad = parseInt(fila.querySelector(".cantidad-producto").value) || 0;
    const total = precio * cantidad;
    fila.querySelector(".total-fila").textContent = total.toFixed(2);
    calcularTotalGeneral();
  }

  // Función para calcular el total general de la tabla
  function calcularTotalGeneral() {
    const filas = document.querySelectorAll("#cuerpo-tabla tr");
    let total = 0;
    filas.forEach(fila => {
      total += parseFloat(fila.querySelector(".total-fila").textContent) || 0;
    });
    document.getElementById("precio-total").textContent = total.toFixed(2);
  }

  // Función para eliminar una fila de la tabla
  function eliminarFila(boton) {
    const fila = boton.closest("tr");
    fila.remove();
    calcularTotalGeneral();
  }



function eliminarFila(boton) {
  const fila = boton.closest("tr");
  fila.remove();
  calcularTotalGeneral();
}

function toggleMenu() {
  const menu = document.getElementById('menu');
  menu.classList.toggle('show');
}