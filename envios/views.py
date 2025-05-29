# envios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db import transaction
from django.urls import reverse
from datetime import datetime
import json
from .models import Producto, Stock, Bodega, GuiaEnvio, GuiaEnvioProducto
from .forms import ProductoForm, StockForm, BodegaForm, GuiaEnvioForm
from django.views.decorators.csrf import csrf_exempt # Make sure this import is present
from decimal import Decimal # Already in your models.py, good to have here if used directly


# Make sure Campaign is included in your model imports
from .models import Producto, Stock, Bodega, GuiaEnvio, GuiaEnvioProducto, Campaign
from .forms import ProductoForm, StockForm, BodegaForm, GuiaEnvioForm

# --- Vistas de Producto, Stock, Bodega (sin cambios) ---
def listar_productos(request):
    search_query = request.GET.get('search', '').strip()
    productos = Producto.objects.all()
    if search_query:
        try:
            id_query = int(search_query)
            productos = productos.filter(Q(id=id_query))
        except ValueError:
            productos = productos.filter(
                Q(nombre__icontains=search_query) | Q(referencia__icontains=search_query)
            )
    return render(request, 'productos/productos.html', {'productos': productos, 'search_query': search_query})

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

def listar_stocks(request):
    stocks = Stock.objects.select_related('producto', 'bodega').all()
    if not stocks.exists():
        messages.info(request, "No hay registros de stock disponibles.")
    return render(request, 'stocks/stocks.html', {'stocks': stocks, 'bodegas': Bodega.objects.all()})

def crear_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            try:
                nuevo_stock = form.save()
                messages.success(request, f"Stock para {nuevo_stock.producto.nombre} creado!")
                return redirect('listar_stocks')
            except Exception as e:
                messages.error(request, f"Error al guardar: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = StockForm()
    return render(request, 'stocks/crear.html', {'form': form, 'productos': Producto.objects.all(), 'bodegas': Bodega.objects.all()})

def editar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock actualizado.')
            return redirect('listar_stocks')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stocks/editar_stock.html', {'form': form})

def eliminar_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Stock eliminado.')
        return redirect('listar_stocks')
    return render(request, 'stocks/eliminar_stock.html', {'stock': stock})

def ver_stock(request, id):
    stock = get_object_or_404(Stock, id=id)
    return render(request, 'stocks/ver_stock.html', {'stock': stock})

def listar_bodegas(request):
    search_query = request.GET.get('search', '').strip()
    bodegas = Bodega.objects.all()
    if search_query:
        try:
            id_query = int(search_query)
            bodegas = bodegas.filter(Q(id=id_query))
        except ValueError:
            bodegas = bodegas.filter(
                Q(nombre__icontains=search_query) | Q(direccion__icontains=search_query) | Q(telefono__icontains=search_query)
            )
    return render(request, 'bodegas/listar_bodegas.html', {'bodegas': bodegas, 'search_query': search_query})

def crear_bodega(request):
    if request.method == 'POST':
        form = BodegaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bodega creada.')
            return redirect('listar_bodegas')
    else:
        form = BodegaForm()
    return render(request, 'bodegas/crear_bodega.html', {'form': form})

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

def eliminar_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    if request.method == 'POST':
        bodega.delete()
        return redirect('listar_bodegas')
    return render(request, 'bodegas/eliminar_bodega.html', {'bodega': bodega})

def ver_bodega(request, id):
    bodega = get_object_or_404(Bodega, id=id)
    return render(request, 'bodegas/ver_bodega.html', {'bodega': bodega})


# --- API VIEWS ---
@require_GET
def search_productos(request):
    search_query = request.GET.get('search', '').strip()
    productos_qs = Producto.objects.all()

    if search_query:
        productos_qs = productos_qs.filter(
            Q(nombre__icontains=search_query) | Q(referencia__icontains=search_query)
        )[:10]
    else:
        productos_qs = Producto.objects.none()

    results = []
    for p in productos_qs:
        results.append({
            'id': p.id,
            'nombre': p.nombre,
            'referencia': p.referencia if p.referencia else '',
            'precio': str(p.precio),
            'imagen': p.imagen.url if p.imagen else None
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


# --- GUIA DE ENVIO VIEWS ---

@transaction.atomic
def crear_guia(request):
    tabla_productos_data_json = '[]' # Default a array JSON vacío
    if request.method == 'POST':
        form = GuiaEnvioForm(request.POST)
        
        productos_en_post_para_repopular = []
        i = 0
        while f'productos[{i}][id]' in request.POST:
            try:
                prod_id = request.POST[f'productos[{i}][id]']
                prod_obj = Producto.objects.get(id=prod_id)
                productos_en_post_para_repopular.append({
                    'id': prod_id,
                    'nombre': request.POST.get(f'productos[{i}][nombre]', prod_obj.nombre),
                    'precio': request.POST.get(f'productos[{i}][precio]', str(prod_obj.precio)), # Precio enviado por el JS
                    'cantidad': request.POST[f'productos[{i}][cantidad]'],
                    'imagen': prod_obj.imagen.url if prod_obj.imagen else 'https://via.placeholder.com/50'
                })
            except Exception: pass
            i += 1
        if productos_en_post_para_repopular:
            tabla_productos_data_json = json.dumps(productos_en_post_para_repopular)

        if form.is_valid():
            try:
                guia = form.save(commit=False)
                items_para_crear_en_db = []
                idx = 0
                hay_productos_en_tabla = False
                primer_producto_obj_de_tabla = None
                primera_cantidad_de_tabla = 1

                while f'productos[{idx}][id]' in request.POST:
                    hay_productos_en_tabla = True
                    producto_id_str = request.POST[f'productos[{idx}][id]']
                    cantidad_str = request.POST[f'productos[{idx}][cantidad]']
                    # Tomar el precio que se envió con el producto en la tabla
                    precio_unitario_str = request.POST.get(f'productos[{idx}][precio]', '0') # Default a '0' si no se encuentra

                    try:
                        producto_id = int(producto_id_str)
                        cantidad_item = int(cantidad_str)
                        precio_unitario = Decimal(precio_unitario_str) # Convertir a Decimal
                        if cantidad_item <= 0: raise ValueError("La cantidad debe ser positiva.")
                        if precio_unitario < 0: raise ValueError("El precio no puede ser negativo.") # Validación básica
                    except ValueError as ve:
                        messages.error(request, f"Error en datos de producto {idx+1} de la tabla: {ve}")
                        return render(request, 'guias/crear_guia.html', {'form': form, 'error_productos': True, 'tabla_productos_data_json': tabla_productos_data_json})

                    producto_obj_item = get_object_or_404(Producto, id=producto_id)
                    if idx == 0:
                        primer_producto_obj_de_tabla = producto_obj_item
                        primera_cantidad_de_tabla = cantidad_item

                    items_para_crear_en_db.append(GuiaEnvioProducto(
                        producto=producto_obj_item,
                        cantidad=cantidad_item,
                        precio_unitario_en_guia=precio_unitario # Usar el precio enviado
                    ))
                    idx += 1
                
                # ... (resto de la lógica de crear_guia como antes) ...
                if not hay_productos_en_tabla:
                    messages.error(request, "Debe agregar al menos un producto a la tabla.")
                    return render(request, 'guias/crear_guia.html', {'form': form, 'error_productos': True, 'tabla_productos_data_json': tabla_productos_data_json})

                if primer_producto_obj_de_tabla:
                    guia.producto = primer_producto_obj_de_tabla
                    guia.cantidad = primera_cantidad_de_tabla
                else:
                    messages.error(request, "Error: No se pudo determinar el producto principal.")
                    return render(request, 'guias/crear_guia.html', {'form': form, 'tabla_productos_data_json': tabla_productos_data_json})
                
                guia.save()

                for item_db in items_para_crear_en_db:
                    item_db.guia_envio = guia
                GuiaEnvioProducto.objects.bulk_create(items_para_crear_en_db)

                messages.success(request, 'Guía creada exitosamente!')
                return redirect('ver_guia', id=guia.id)

            # ... (except blocks como antes) ...
            except Producto.DoesNotExist:
                messages.error(request, 'Error: Uno de los productos seleccionados no existe.')
                return render(request, 'guias/crear_guia.html', {'form': form, 'error_productos': True, 'tabla_productos_data_json': tabla_productos_data_json})
            except Exception as e:
                messages.error(request, f'Error inesperado al crear la guía: {str(e)}')
                return render(request, 'guias/crear_guia.html', {'form': form, 'tabla_productos_data_json': tabla_productos_data_json})

        else: # Formulario principal no válido
            error_list = []
            for field, errors in form.errors.items():
                field_label = form.fields[field].label if field in form.fields and hasattr(form.fields[field], 'label') and form.fields[field].label else field
                for error in errors: error_list.append(f"Error en '{field_label}': {error}")
            messages.error(request, f"Por favor corrige los errores: {'; '.join(error_list)}")
            return render(request, 'guias/crear_guia.html', {'form': form, 'tabla_productos_data_json': tabla_productos_data_json})
    else: # GET request
        form = GuiaEnvioForm()
    
    return render(request, 'guias/crear_guia.html', {'form': form, 'tabla_productos_data_json': tabla_productos_data_json})

# La función editar_guia necesitaría una adaptación similar para tomar `precio_unitario_str`
# del `request.POST[f'productos[{idx}][precio]']` al reconstruir `items_nuevos_para_db`.

@transaction.atomic
def editar_guia(request, id):
    guia = get_object_or_404(
        GuiaEnvio.objects.select_related('producto').prefetch_related('items_guia__producto'),
        id=id
    )
    # Para la carga inicial de la página de edición
    items_actuales_original_json = json.dumps([
        {
            'id': str(item.producto.id), 'nombre': item.producto.nombre,
            'imagen': item.producto.imagen.url if item.producto.imagen else 'https://via.placeholder.com/50',
            'precio': str(item.precio_unitario_en_guia), 'cantidad': item.cantidad
        } for item in guia.items_guia.all()
    ])
    tabla_post_data_json = None # Para repopular si el form principal falla en POST

    if request.method == 'POST':
        form = GuiaEnvioForm(request.POST, instance=guia)
        # Capturar datos de la tabla del POST
        productos_en_post_para_repopular = []
        i = 0
        while f'productos[{i}][id]' in request.POST:
            try:
                producto_id = request.POST[f'productos[{i}][id]']
                producto_obj_temp = Producto.objects.get(id=producto_id)
                productos_en_post_para_repopular.append({
                    'id': producto_id,
                    'nombre': request.POST.get(f'productos[{i}][nombre]', producto_obj_temp.nombre),
                    'precio': request.POST.get(f'productos[{i}][precio]', str(producto_obj_temp.precio)),
                    'cantidad': request.POST[f'productos[{i}][cantidad]'],
                    'imagen': producto_obj_temp.imagen.url if producto_obj_temp.imagen else 'https://via.placeholder.com/50'
                })
            except: pass # Ignorar errores al recolectar para repopulación
            i += 1
        if productos_en_post_para_repopular:
            tabla_post_data_json = json.dumps(productos_en_post_para_repopular)


        if form.is_valid():
            try:
                guia_actualizada = form.save(commit=False)
                items_nuevos_para_db = []
                idx = 0
                hay_productos_en_tabla = False
                primer_producto_obj_de_tabla_post = None
                primera_cantidad_de_tabla_post = 1

                while f'productos[{idx}][id]' in request.POST:
                    hay_productos_en_tabla = True
                    producto_id_str = request.POST[f'productos[{idx}][id]']
                    cantidad_str = request.POST[f'productos[{idx}][cantidad]']
                    try:
                        producto_id = int(producto_id_str)
                        cantidad_item = int(cantidad_str)
                        if cantidad_item <= 0:
                            raise ValueError("Cantidad debe ser positiva.")
                    except ValueError as ve:
                        messages.error(request, f"Datos inválidos para el producto {idx+1} en la tabla: {ve}")
                        return render(request, 'guias/editar_guia.html', {'form': form, 'guia': guia, 'items_actuales_json': tabla_post_data_json if tabla_post_data_json else items_actuales_original_json, 'error_productos': True})

                    producto_obj_item = get_object_or_404(Producto, id=producto_id)
                    if idx == 0:
                        primer_producto_obj_de_tabla_post = producto_obj_item
                        primera_cantidad_de_tabla_post = cantidad_item

                    items_nuevos_para_db.append(
                        GuiaEnvioProducto(
                            guia_envio=guia_actualizada,
                            producto=producto_obj_item,
                            cantidad=cantidad_item,
                            precio_unitario_en_guia=producto_obj_item.precio
                        )
                    )
                    idx += 1

                if not hay_productos_en_tabla:
                    messages.error(request, "Debe haber al menos un producto en la tabla.")
                    return render(request, 'guias/editar_guia.html', {'form': form, 'guia': guia, 'items_actuales_json': tabla_post_data_json if tabla_post_data_json else items_actuales_original_json, 'error_productos': True})

                if primer_producto_obj_de_tabla_post:
                    guia_actualizada.producto = primer_producto_obj_de_tabla_post
                    guia_actualizada.cantidad = primera_cantidad_de_tabla_post
                else:
                    guia_actualizada.producto = None
                    guia_actualizada.cantidad = None

                guia_actualizada.save()
                guia.items_guia.all().delete()
                if items_nuevos_para_db:
                    GuiaEnvioProducto.objects.bulk_create(items_nuevos_para_db)

                messages.success(request, f'Guía #{guia.id} actualizada correctamente.')
                return redirect('ver_guia', id=guia.id)
            except Exception as e:
                messages.error(request, f"Error al actualizar la guía: {str(e)}")
                return render(request, 'guias/editar_guia.html', {'form': form, 'guia': guia, 'items_actuales_json': tabla_post_data_json if tabla_post_data_json else items_actuales_original_json})
        else: # Si form principal no es válido
            error_list = []
            for field, errors_list_form in form.errors.items():
                field_label = form.fields[field].label if field in form.fields and hasattr(form.fields[field], 'label') and form.fields[field].label else field
                for error_item in errors_list_form:
                    error_list.append(f"Error en '{field_label}': {error_item}")
            messages.error(request, f"Por favor corrige los errores en el formulario principal: {'; '.join(error_list)}")
            return render(request, 'guias/editar_guia.html', {
                'form': form,
                'guia': guia,
                'items_actuales_json': tabla_post_data_json if tabla_post_data_json else items_actuales_original_json
            })
    else: # GET request
        form = GuiaEnvioForm(instance=guia)

    return render(request, 'guias/editar_guia.html', {
        'form': form,
        'guia': guia,
        'items_actuales_json': items_actuales_original_json
    })


def ver_guia(request, id):
    guia = get_object_or_404(
        GuiaEnvio.objects.select_related('producto').prefetch_related('items_guia__producto'),
        id=id
    )
    return render(request, 'guias/ver_guia.html', {
        'guia': guia,
        'estados': GuiaEnvio.ESTADO_CHOICES
    })

def eliminar_guia(request, id):
    guia = get_object_or_404(GuiaEnvio, id=id)
    if request.method == 'POST':
        guia_id_display = guia.id
        guia.delete()
        messages.success(request, f'Guía #{guia_id_display} eliminada correctamente.')
        return redirect('listar_guias')
    return render(request, 'guias/eliminar_guia.html', {'guia': guia})

def listar_guias(request):
    guias_qs = GuiaEnvio.objects.select_related('producto').prefetch_related(
        'items_guia__producto'
    ).all().order_by('-fecha_creacion')

    estado_filter = request.GET.get('estado', '')
    ciudad_filter = request.GET.get('ciudad', '')
    search_query = request.GET.get('search', '').strip()
    fecha_inicio_str = request.GET.get('fecha_inicio', '')
    fecha_fin_str = request.GET.get('fecha_fin', '')

    if estado_filter:
        guias_qs = guias_qs.filter(estado=estado_filter)
    if ciudad_filter:
        guias_qs = guias_qs.filter(cliente_ciudad=ciudad_filter)

    if fecha_inicio_str:
        try:
            fecha_inicio_obj = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            guias_qs = guias_qs.filter(fecha_creacion__date__gte=fecha_inicio_obj)
        except ValueError:
            messages.warning(request, "Formato de fecha de inicio inválido. Use YYYY-MM-DD.")
    if fecha_fin_str:
        try:
            fecha_fin_obj = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            guias_qs = guias_qs.filter(fecha_creacion__date__lte=fecha_fin_obj)
        except ValueError:
            messages.warning(request, "Formato de fecha de fin inválido. Use YYYY-MM-DD.")

    if search_query:
        try:
            search_id = int(search_query)
            id_query = Q(id=search_id)
        except ValueError:
            id_query = Q()

        guias_qs = guias_qs.filter(
            id_query |
            Q(cliente_nombre__icontains=search_query) |
            Q(codigo_seguimiento__icontains=search_query) |
            Q(producto__nombre__icontains=search_query) |
            Q(items_guia__producto__nombre__icontains=search_query) |
            Q(contenido_resumen__icontains=search_query)
        ).distinct()

    todas_las_ciudades_en_db = GuiaEnvio.objects.values_list('cliente_ciudad', flat=True).distinct().order_by('cliente_ciudad')
    ciudades_dropdown_choices = [(ciudad, ciudad) for ciudad in todas_las_ciudades_en_db if ciudad]

    context = {
        'guias': guias_qs,
        'estados': GuiaEnvio.ESTADO_CHOICES,
        'ciudades': ciudades_dropdown_choices,
        'estado_selected': estado_filter,
        'ciudad_selected': ciudad_filter,
        'search_query': search_query,
        'fecha_inicio_selected': fecha_inicio_str,
        'fecha_fin_selected': fecha_fin_str,
    }
    return render(request, 'guias/listar_guias.html', context)

    #campañas


# --- Vistas de Producto, Stock, Bodega (sin cambios) ---
# ... (your existing views for Producto, Stock, Bodega) ...

# --- API VIEWS ---
# ... (your existing API views search_productos, producto_detail_api) ...

# --- GUIA DE ENVIO VIEWS ---
# ... (your existing Guia de Envio views: crear_guia, editar_guia, ver_guia, eliminar_guia, listar_guias) ...

#campañas
def index(request):
    # This block needs to be indented
    context = {
        'countries': [
            {'code': 'COL', 'name': 'Colombia'},
            {'code': 'ECU', 'name': 'Ecuador'},
            {'code': 'VEN', 'name': 'Venezuela'}
        ],
        'platforms': [
            {'name': 'Facebook', 'code': 'F'},
            {'name': 'TikTok', 'code': 'T'}
        ],
        'campaign_types': [
            {'name': 'CBO', 'desc': 'Campaign Budget Optimization'},
            {'name': 'ABO', 'desc': 'Ad Set Budget'}
        ],
        'persons': [
            {'initials': 'DP', 'name': 'David Pérez'},
            {'initials': 'AC', 'name': 'Ana Contreras'},
            {'initials': 'MR', 'name': 'Mario Rodríguez'}
        ]
    }
    return render(request, 'campaigns/index.html', context)

def saved_campaigns(request):
    # This block needs to be indented
    campaigns = Campaign.objects.all()
    return render(request, 'campaigns/campanas_guardadas.html', {'campaigns': campaigns})

@csrf_exempt
def save_campaign(request):
    # This block needs to be indented
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            gui_string = data.get('gui_string')
            
            if Campaign.objects.filter(gui_string=gui_string).exists():
                return JsonResponse({'success': False, 'error': 'Esta campaña ya existe'})
                
            campaign = Campaign(
                gui_string=gui_string,
                pais=data.get('pais'),
                plataforma=data.get('plataforma'),
                tipo_campana=data.get('tipo_campana'),
                fecha=data.get('fecha'),
                nombre_reloj=data.get('nombre_reloj'),
                id_reloj=data.get('id_reloj'),
                persona=data.get('persona'),
                num_importacion=data.get('num_importacion')
            )
            campaign.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def clear_campaigns(request):
    # This block needs to be indented
    if request.method == 'POST':
        try:
            Campaign.objects.all().delete()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})