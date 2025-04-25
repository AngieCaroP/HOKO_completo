from django.contrib import admin
from .models import Producto

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'referencia', 'costo', 'precio')
    search_fields = ('nombre', 'referencia')



