# envios/models.py

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

#guias
class GuiaEnvio(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparación'),
        ('transito', 'En tránsito'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    CIUDAD_CHOICES = [
        ('Guayaquil', 'Guayaquil'),
        ('Quito', 'Quito'),
        # Agrega más ciudades si necesitas
    ]

    # Datos del cliente
    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20)
    cliente_ciudad = models.CharField(
        max_length=50,
        choices=CIUDAD_CHOICES,
        verbose_name='Ciudad'
    )
    cliente_direccion = models.TextField()
    cliente_direccion2 = models.TextField(blank=True, null=True)

    # Relación con productos
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='guias')
    cantidad = models.PositiveIntegerField(default=1)
    contenido = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    # Seguimiento
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    codigo_seguimiento = models.CharField(max_length=20, unique=True, blank=True)
    # Campos de fecha/hora con auto_now_add y auto_now
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de modificación")

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Guía de Envío'
        verbose_name_plural = 'Guías de Envío'

    def __str__(self):
        return f"Guía #{self.id} - {self.cliente_nombre}"

    def get_absolute_url(self):
        return reverse('ver_guia', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            self.codigo_seguimiento = f"TEMP-{self.id}" if self.id else "TEMP-CODE"
        super().save(*args, **kwargs)

        if self.codigo_seguimiento.startswith("TEMP-CODE") and self.id:
            self.codigo_seguimiento = f"HOKO-{self.id:05d}"
            super().save(update_fields=['codigo_seguimiento'])