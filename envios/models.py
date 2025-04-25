

from django.db import models
from decimal import Decimal

# Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def __str__(self):
        return self.nombre
# envios/models.py
# Bodega Stock
class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

# Stock
class Stock(models.Model):
    """Modelo que representa el stock de un producto en una bodega específica."""
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    stock_actual = models.IntegerField(default=0)
    umbral_minimo = models.IntegerField(default=0)
    
    ESTADOS = (
        ('sin_stock', 'Sin stock'),
        ('stock_bajo', 'Stock bajo'),
        ('en_stock', 'En stock'),
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='en_stock')
    
    def save(self, *args, **kwargs):
        """
        Actualiza automáticamente el estado del stock según la cantidad disponible
        antes de guardar en la base de datos.
        """
        if self.stock_actual <= 0:
            self.estado = 'sin_stock'
        elif self.stock_actual < self.umbral_minimo:
            self.estado = 'stock_bajo'
        else:
            self.estado = 'en_stock'
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Representación en string del registro de stock."""
        return f"{self.producto} - {self.bodega}"
