// Función para calcular el total de una fila
function calcularFila(input) {
  const fila = input.closest("tr");
  const precio = parseFloat(fila.querySelector(".precio-producto").value) || 0;
  const cantidad = parseInt(fila.querySelector(".cantidad-producto").value) || 0;
  const total = precio * cantidad;
  fila.querySelector(".total-fila").textContent = total.toFixed(2);
  calcularTotalGeneral();
}

// Función para calcular el total general
function calcularTotalGeneral() {
  const filas = document.querySelectorAll("#cuerpo-tabla tr");
  let total = 0;
  filas.forEach(fila => {
    total += parseFloat(fila.querySelector(".total-fila").textContent) || 0;
  });
  document.getElementById("precio-total").textContent = total.toFixed(2);
}

// Función para eliminar una fila
function eliminarFila(boton) {
  const fila = boton.closest("tr");
  fila.remove();
  calcularTotalGeneral();
  // También puedes limpiar el select de producto si es necesario
  document.querySelector('select[name="producto"]').value = '';
}