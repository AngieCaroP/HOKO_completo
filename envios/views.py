# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Producto, Stock, Bodega, GuiaEnvio
from .forms import ProductoForm, StockForm, BodegaForm, GuiaEnvioForm
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import json


# ===== PRODUCTOS =====
def listar_productos(request):
    search_query = request.GET.get('search', '').strip()
    
    productos = Producto.objects.all()
    
    if search_query:
        try:
            # Intentar buscar por ID (si el query es numérico)
            id_query = int(search_query)
            productos = productos.filter(Q(id=id_query))
        except ValueError:
            # Si no es numérico, buscar por nombre o referencia
            productos = productos.filter(
                Q(nombre__icontains=search_query) |
                Q(referencia__icontains=search_query)
            )
    
    return render(request, 'productos/productos.html', {
        'productos': productos,
        'search_query': search_query
    })

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
    search_query = request.GET.get('search', '').strip()
    
    bodegas = Bodega.objects.all()
    
    if search_query:
        try:
            # Intentar buscar por ID (si el query es numérico)
            id_query = int(search_query)
            bodegas = bodegas.filter(Q(id=id_query))
        except ValueError:
            # Si no es numérico, buscar por nombre, dirección o teléfono
            bodegas = bodegas.filter(
                Q(nombre__icontains=search_query) |
                Q(direccion__icontains=search_query) |
                Q(telefono__icontains=search_query)
            )
    
    return render(request, 'bodegas/listar_bodegas.html', {
        'bodegas': bodegas,
        'search_query': search_query
    })

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

#=======guias========

def crear_guia(request):
    if request.method == 'POST':
        form = GuiaEnvioForm(request.POST)
        if form.is_valid():
            try:
                guia = form.save(commit=False)
                
                # Asegurar que el estado tenga un valor si no se proporcionó
                if not guia.estado:
                    guia.estado = 'pendiente'
                
                # Aquí podrías asignar el usuario si quieres:
                # if request.user.is_authenticated:
                #     guia.usuario_creacion = request.user

                guia.save()

                messages.success(request, f'Guía #{guia.id} creada exitosamente! Código: {guia.codigo_seguimiento}')
                return redirect('ver_guia', id=guia.id)
            except Exception as e:
                messages.error(request, f'Error al crear la guía: {str(e)}')
        else:
            # Mostrar errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        # Cuando es GET, inicializar el formulario
        form = GuiaEnvioForm(initial={'estado': 'pendiente'})

    # Cargar productos para mostrar en la plantilla
    productos = Producto.objects.all()
    query = request.GET.get('q', '')

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(referencia__icontains=query)
        )

    return render(request, 'guias/crear_guia.html', {
        'form': form,
        'productos': productos,
        'query': query
    })

def ver_guia(request, id):
    guia = get_object_or_404(GuiaEnvio, id=id)
    return render(request, 'guias/ver_guia.html', {
        'guia': guia,
        'estados': GuiaEnvio.ESTADO_CHOICES
    })

def listar_guias(request):
    guias = GuiaEnvio.objects.select_related('producto').all().order_by('-fecha_creacion')

    estado = request.GET.get('estado', '')
    ciudad = request.GET.get('ciudad', '')
    search_query = request.GET.get('search', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    # Filtros individuales
    if estado:
        guias = guias.filter(estado=estado)
    if ciudad:
        guias = guias.filter(cliente_ciudad=ciudad)

    if search_query:
        guias = guias.filter(
            Q(cliente_nombre__icontains=search_query) |
            Q(codigo_seguimiento__icontains=search_query) |
            Q(producto__nombre__icontains=search_query)
        )

    if fecha_inicio:
        guias = guias.filter(fecha_creacion__gte=fecha_inicio)
    if fecha_fin:
        from datetime import datetime, timedelta
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d') + timedelta(days=1)
        guias = guias.filter(fecha_creacion__lte=fecha_fin_dt)

    ciudades = set(GuiaEnvio.objects.values_list('cliente_ciudad', flat=True).distinct())
    ciudades_choices = [(ciudad, ciudad) for ciudad in ciudades]

    return render(request, 'guias/listar_guias.html', {
        'guias': guias,
        'estados': GuiaEnvio.ESTADO_CHOICES,
        'ciudades': sorted(ciudades_choices, key=lambda x: x[1]),
        'estado_selected': estado,
        'ciudad_selected': ciudad,
        'search_query': search_query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })


def editar_guia(request, id):
    guia = get_object_or_404(GuiaEnvio, id=id)
    if request.method == 'POST':
        form = GuiaEnvioForm(request.POST, instance=guia)
        if form.is_valid():
            form.save()
            messages.success(request, f'Guía #{guia.id} actualizada correctamente.')
            return redirect('ver_guia', id=guia.id)
    else:
        form = GuiaEnvioForm(instance=guia)
    
    return render(request, 'guias/editar_guia.html', {
        'form': form,
        'guia': guia
    })

def eliminar_guia(request, id):
    guia = get_object_or_404(GuiaEnvio, id=id)
    if request.method == 'POST':
        guia_id = guia.id
        guia.delete()
        messages.success(request, f'Guía #{guia_id} eliminada correctamente.')
        return redirect('listar_guias')
    
    return render(request, 'guias/eliminar_guia.html', {'guia': guia})


@require_GET
def producto_api_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'referencia': producto.referencia if hasattr(producto, 'referencia') else '',
        'precio': str(producto.precio),
        'imagen': producto.imagen.url if producto.imagen else None,
    }
    return JsonResponse(data)


#api para productos 
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from .models import Producto

@require_GET
def search_productos(request):
    search_query = request.GET.get('search', '').strip()
    
    productos = Producto.objects.all()
    
    if search_query:
        productos = productos.filter(
            Q(nombre__icontains=search_query) |
            Q(referencia__icontains=search_query)
        )[:10]  # Limitar a 10 resultados
    
    results = []
    for producto in productos:
        results.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'referencia': producto.referencia,
            'precio': str(producto.precio),
            'imagen': producto.imagen.url if producto.imagen else None,
        })
    
    return JsonResponse(results, safe=False)

@require_GET
def producto_detail_api(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'referencia': producto.referencia,
        'precio': str(producto.precio),
        'imagen': producto.imagen.url if producto.imagen else None,
    }
    return JsonResponse(data)