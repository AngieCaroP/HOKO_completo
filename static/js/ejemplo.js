document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('producto-search');
    const resultsContainer = document.getElementById('producto-results');
    const productoIdInput = document.getElementById('id_producto');
    const selectedProductContainer = document.getElementById('selected-product');
    
    // Función para buscar productos
    function searchProductos(query) {
        if (query.length < 2) {
            resultsContainer.style.display = 'none';
            return;
        }
        
        fetch(`/api/productos/?search=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    resultsContainer.innerHTML = '';
                    data.forEach(producto => {
                        const item = document.createElement('div');
                        item.className = 'producto-item';
                        item.innerHTML = `
                            <img src="${producto.imagen || 'https://via.placeholder.com/50'}" 
                                 onerror="this.src='https://via.placeholder.com/50'">
                            <div class="producto-info">
                                <strong>${producto.nombre}</strong>
                                <div>
                                    <small>Ref: ${producto.referencia || 'N/A'}</small> | 
                                    <strong>$${producto.precio}</strong>
                                </div>
                            </div>
                        `;
                        
                        item.addEventListener('click', function() {
                            selectProducto(producto);
                        });
                        
                        resultsContainer.appendChild(item);
                    });
                    resultsContainer.style.display = 'block';
                } else {
                    resultsContainer.style.display = 'none';
                }
            });
    }
    
    // Función para seleccionar un producto
    function selectProducto(producto) {
        productoIdInput.value = producto.id;
        searchInput.value = producto.nombre;
        
        // Mostrar detalles del producto seleccionado
        document.getElementById('selected-product-img').src = producto.imagen || 'https://via.placeholder.com/100';
        document.getElementById('selected-product-name').textContent = producto.nombre;
        document.getElementById('selected-product-ref').textContent = producto.referencia || 'N/A';
        document.getElementById('selected-product-price').textContent = producto.precio;
        selectedProductContainer.style.display = 'block';
        
        resultsContainer.style.display = 'none';
    }
    
    // Event listeners
    searchInput.addEventListener('input', function() {
        searchProductos(this.value);
    });
    
    // Ocultar resultados al hacer clic fuera
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
            resultsContainer.style.display = 'none';
        }
    });
    
    // Si ya hay un producto seleccionado (en caso de edición)
    {% if form.producto.value %}
    fetch(`/api/productos/{{ form.producto.value }}/`)
        .then(response => response.json())
        .then(producto => {
            if (producto) {
                selectProducto(producto);
            }
        });
    {% endif %}


    
});

