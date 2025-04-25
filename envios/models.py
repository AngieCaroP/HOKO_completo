from django.db import models
from decimal import Decimal
from django.utils import timezone


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def __str__(self):
        return self.nombre


class Bodega(models.Model):
    """Modelo que representa una bodega o almacén."""
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    
    def __str__(self):
        """Representación en string de la bodega."""
        return f"{self.nombre} - {self.ubicacion}"


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



class Transportadora(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    
    def __str__(self):
        return self.nombre

class GuiaEnvio(models.Model):
    ESTADOS = (
        ('activa', 'Activa'),
        ('en_transito', 'En tránsito'),
        ('entregada', 'Entregada'),
    )
    
    numero_guia = models.CharField(max_length=20, unique=True)
    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20)
    cliente_ciudad = models.CharField(max_length=50)
    cliente_direccion = models.TextField()
    contenido = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    transportadora = models.ForeignKey(Transportadora, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activa')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Guía {self.numero_guia} - {self.cliente_nombre}"
    
    def save(self, *args, **kwargs):
        if not self.numero_guia:
            # Generar número de guía automático
            last_guia = GuiaEnvio.objects.order_by('-id').first()
            last_id = last_guia.id if last_guia else 0
            self.numero_guia = f"HO{str(last_id + 1).zfill(6)}"
        super().save(*args, **kwargs)

    