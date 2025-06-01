from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:id>/', views.ver_producto, name='ver_producto'),
    path('productos/<int:id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),

    path('stocks/', views.listar_stocks, name='listar_stocks'),
    path('stocks/crear/', views.crear_stock, name='crear_stock'),
    path('stocks/<int:id>/', views.ver_stock, name='ver_stock'),
    path('stocks/<int:id>/editar/', views.editar_stock, name='editar_stock'),
    path('stocks/<int:id>/eliminar/', views.eliminar_stock, name='eliminar_stock'),

    path('bodegas/', views.listar_bodegas, name='listar_bodegas'),
    path('bodegas/crear/', views.crear_bodega, name='crear_bodega'),
    path('bodegas/<int:id>/', views.ver_bodega, name='ver_bodega'),
    path('bodegas/editar/<int:id>/', views.editar_bodega, name='editar_bodega'),
    path('bodegas/eliminar/<int:id>/', views.eliminar_bodega, name='eliminar_bodega'),

    path('guias/', views.listar_guias, name='listar_guias'),
    path('guias/crear/', views.crear_guia, name='crear_guia'),
    path('guias/<int:id>/', views.ver_guia, name='ver_guia'),
    path('guias/<int:id>/editar/', views.editar_guia, name='editar_guia'),
    path('guias/<int:id>/eliminar/', views.eliminar_guia, name='eliminar_guia'),

    path('api/productos/', views.search_productos, name='search_productos_api'),
    path('api/productos/<int:pk>/', views.producto_detail_api, name='producto_detail_api'),
    
    # --- CAMPAÑAS ---
    # Asegúrate que 'views.index' corresponda al nombre correcto en views.py 
    # (si lo renombraste a 'index_campaigns', cámbialo aquí también)
    path('campaigns/', views.index, name='index'), 
    path('campaigns/campanas_guardadas/', views.saved_campaigns, name='campanas_guardadas'),
    
    # --- CORRECCIÓN PARA EL AttributeError ---
    path('api/save-campaign/', views.save_campaign_api, name='save_campaign_api'),
    path('api/clear-campaigns/', views.clear_campaigns_api, name='clear_campaigns_api'),
    # --- FIN DE LA CORRECCIÓN ---
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)