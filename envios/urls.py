# envios/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/<int:id>/', views.ver_producto, name='ver_producto'),
    path('productos/<int:id>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:id>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
 
    path('stocks/', views.listar_stocks, name='listar_stocks'),
    path('stocks/crear/', views.crear_stock, name='crear_stock'),
    path('stocks/<int:id>/editar/', views.editar_stock, name='editar_stock'), 
    path('stocks/<int:id>/eliminar/', views.eliminar_stock, name='eliminar_stock'),


]

