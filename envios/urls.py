# envios/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    # Productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:id>/', views.ver_producto, name='ver_producto'),
    path('productos/<int:id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
 
    # Stocks
    path('stocks/', views.listar_stocks, name='listar_stocks'),
    path('stocks/crear/', views.crear_stock, name='crear_stock'),
    path('stocks/<int:id>/', views.ver_stock, name='ver_stock'),  # Nueva ruta
    path('stocks/<int:id>/editar/', views.editar_stock, name='editar_stock'), 
    path('stocks/<int:id>/eliminar/', views.eliminar_stock, name='eliminar_stock'),

    # Bodegas
    path('bodegas/', views.listar_bodegas, name='listar_bodegas'),
    path('bodegas/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodegas/<int:id>/', views.ver_bodega, name='ver_bodega'),  # Nueva ruta
    path('bodegas/editar/<int:id>/', views.editar_bodega, name='editar_bodega'),
    path('bodegas/eliminar/<int:id>/', views.eliminar_bodega, name='eliminar_bodega'),

      # Guías
    path('guias/', views.listar_guias, name='listar_guias'),
    path('guias/crear/', views.crear_guia, name='crear_guia'),
    path('guias/<int:id>/', views.ver_bodega, name='ver_guia'),  # Nueva ruta
    path('guias/editar/<int:id>/', views.editar_bodega, name='editar_guia'),
    path('guias/eliminar/<int:id>/', views.eliminar_bodega, name='eliminar_guia'),
    
    # API
    path('api/productos/<int:pk>/', views.producto_api_detail, name='producto_api_detail'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

