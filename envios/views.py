# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Stock,  Bodega
from .forms import ProductoForm, StockForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .forms import BodegaForm


#productos

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

def ver_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'ver_producto.html', {'producto': producto})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form})

def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if request.method == 'POST':
        producto.delete()
        messages.success(request, f'Producto "{producto.nombre}" eliminado correctamente.')
        return redirect('listar_productos')
        
    return render(request, 'eliminar_producto.html', {'producto': producto})

#stock 

def listar_stocks(request):
    stocks = Stock.objects.select_related('producto', 'bodega').all()
    return render(request, 'stocks.html', {
        'stocks': stocks,
        'productos': Producto.objects.all(),
        'bodegas': Bodega.objects.all()
    })

from django.shortcuts import render, redirect, get_object_or_404
from .models import Stock
from .forms import StockForm

def listar_stocks(request):  # Esta función debe existir
    stocks = Stock.objects.all()
    return render(request, 'stocks.html', {'stocks': stocks})

def crear_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_stocks')
    else:
        form = StockForm()
    return render(request, 'crear.html', {'form': form})

def editar_stock(request, id):  # ¡Esta es la función faltante!
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('listar_stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'editar_stock.html', {'form': form})

def eliminar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        stock.delete()
        return redirect('listar_stocks')
    return render(request, 'eliminar_stock.html', {'stock': stock})

#bodegas

# Vista para crear una nueva bodega
def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_bodegas')  # Redirige a la lista de bodegas después de guardar
    else:
        form = BodegaForm()  # Si no es POST, mostramos el formulario vacío
    return render(request, 'crear_bodega.html', {'form': form})

# Vista para listar todas las bodegas
def listar_bodegas(request):
    bodegas = Bodega.objects.all()  # Recupera todas las bodegas de la base de datos
    return render(request, 'listar_bodegas.html', {'bodegas': bodegas})

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
    return render(request, 'editar_bodega.html', {'form': form})

# Vista para eliminar una bodega
def eliminar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    if request.method == 'POST':
        bodega.delete()
        return redirect('listar_bodegas')
    return render(request, 'eliminar_bodega.html', {'bodega': bodega})