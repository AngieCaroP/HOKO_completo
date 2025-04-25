# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Stock, GuiaEnvio, Bodega, Transportadora
from .forms import ProductoForm, StockForm, GuiaEnvioForm, BodegaForm, TransportadoraForm
from .forms import GuiaEnvioForm
from django.contrib import messages
from django.db.models import Q



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

def crear_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_stocks')
    else:
        form = StockForm()
    return render(request, 'crear.html', {'form': form})

def actualizar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            return redirect('listar_stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'editar.html', {'form': form})

def eliminar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        stock.delete()
        return redirect('listar_stocks')
    return render(request, 'eliminar.html', {'stock': stock})


#nose

def gestion_bodegas(request):
    bodegas = Bodega.objects.all()
    form = BodegaForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('gestion_bodegas')
    
    return render(request, 'bodegas.html', {
        'bodegas': bodegas,
        'form': form
    })

