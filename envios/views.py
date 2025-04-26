# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Stock,  Bodega
from .forms import ProductoForm, StockForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import BodegaForm

# ===== PRODUCTOS =====
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

def ver_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'productos/ver_producto.html', {'producto': producto})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
        return redirect('listar_productos')
        
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

# ===== STOCKS =====
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Bodega, Stock
from .forms import StockForm

def listar_stocks(request):
    try:
        # Obtener todos los stocks con información relacionada
        stocks = Stock.objects.select_related('producto', 'bodega').all()
        
        # Verificar si hay datos
        if not stocks.exists():
            messages.info(request, "No hay registros de stock disponibles.")
        
        return render(request, 'stocks/stocks.html', {
            'stocks': stocks,
            'bodegas': Bodega.objects.all()  # Para filtros
        })
        
    except Exception as e:
        messages.error(request, f"Error al cargar los stocks: {str(e)}")
        return render(request, 'stocks/stocks.html', {'stocks': []})

def crear_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            try:
                nuevo_stock = form.save()
                messages.success(request, f"Stock para {nuevo_stock.producto.nombre} creado correctamente!")
                return redirect('listar_stocks')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            # Muestra errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = StockForm()
    
    # Asegúrate de pasar productos y bodegas al contexto
    return render(request, 'stocks/crear.html', {
        'form': form,
        'productos': Producto.objects.all(),
        'bodegas': Bodega.objects.all()
    })

def editar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock actualizado correctamente.')
            return redirect('listar_stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stocks/editar_stock.html', {'form': form})

def eliminar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Stock eliminado correctamente.')
        return redirect('listar_stocks')
    return render(request, 'stocks/eliminar_stock.html', {'stock': stock})

def ver_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    return render(request, 'stocks/ver_stock.html', {'stock': stock})


# ===== BODEGAS =====
def listar_bodegas(request):
    bodegas = Bodega.objects.all()
    return render(request, 'bodegas/listar_bodegas.html', {'bodegas': bodegas})

def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada correctamente.')
            return redirect('listar_bodegas')
    else:
        form = BodegaForm()
    return render(request, 'bodegas/crear_bodega.html', {'form': form})

# Vista para editar una bodega existente
def editar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            return redirect('listar_bodegas')
    else:
        form = BodegaForm(instance=bodega)
    return render(request, 'bodegas/editar_bodega.html', {'form': form})

# Vista para eliminar una bodega
def eliminar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    if request.method == 'POST':
        bodega.delete()
        return redirect('listar_bodegas')
    return render(request, 'bodegas/eliminar_bodega.html', {'bodega': bodega})

def ver_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    return render(request, 'bodegas/ver_bodega.html', {'bodega': bodega})
