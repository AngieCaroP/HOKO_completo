#envios/models.py
from django.db import models
from decimal import Decimal
from django.urls import reverse

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    referencia = models.CharField(max_length=50, blank=True, null=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return self.nombre

class Bodega(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    stock_actual = models.IntegerField()
    umbral_minimo = models.IntegerField()
    ESTADO_CHOICES = [
        ('ok', 'Stock OK'),
        ('bajo', 'Stock Bajo'),
        ('sin', 'Sin Stock'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, editable=False, default='ok')

    def save(self, *args, **kwargs):
        if self.stock_actual <= 0:
            self.estado = 'sin'
        elif self.stock_actual < self.umbral_minimo:
            self.estado = 'bajo'
        else:
            self.estado = 'ok'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} - {self.bodega.nombre} - {self.stock_actual}"

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
    ]

    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20)
    cliente_ciudad = models.CharField(max_length=50, choices=CIUDAD_CHOICES, verbose_name='Ciudad')
    cliente_direccion = models.TextField()
    cliente_direccion2 = models.TextField(blank=True, null=True)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT,
        related_name='guias_como_principal',
        null=True, blank=True,
        verbose_name="Producto Principal (Automático)"
    )
    cantidad = models.PositiveIntegerField(
        default=1, null=True, blank=True,
        verbose_name="Cantidad Principal (Automático)"
    )
    contenido_resumen = models.CharField(max_length=500, blank=True, null=True, help_text="Resumen textual de los productos de la tabla.")
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    codigo_seguimiento = models.CharField(max_length=20, unique=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha y hora de modificación")

    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Guía de Envío'
        verbose_name_plural = 'Guías de Envío'

    def __str__(self):
        return f"Guía #{self.id or 'Nueva'} - {self.cliente_nombre}"

    def get_absolute_url(self):
        return reverse('ver_guia', args=[str(self.id)])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new and not self.codigo_seguimiento:
            if not getattr(self, '_saving_code', False):
                self._saving_code = True
                super().save(*args, **{k:v for k,v in kwargs.items() if k != 'update_fields'})
                self.codigo_seguimiento = f"HOKO-{self.id:05d}"
                super().save(update_fields=['codigo_seguimiento'])
                del self._saving_code
                return
        super().save(*args, **kwargs)

    @property
    def total_guia(self):
        if hasattr(self, 'items_guia') and self.items_guia.exists():
            return sum(item.subtotal for item in self.items_guia.all())
        return Decimal('0.00')

class GuiaEnvioProducto(models.Model):
    guia_envio = models.ForeignKey(GuiaEnvio, related_name='items_guia', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario_en_guia = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto al momento de crear la guía")

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario_en_guia

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Guía #{self.guia_envio.id if self.guia_envio_id else 'Nueva'}"

    class Meta:
        unique_together = ('guia_envio', 'producto')
        verbose_name = "Producto en Guía de Envío"
        verbose_name_plural = "Productos en Guías de Envío"


    #campañas
class Campaign(models.Model):
    gui_string = models.CharField(max_length=255, unique=True)
    pais = models.CharField(max_length=3)
    plataforma = models.CharField(max_length=1)
    tipo_campana = models.CharField(max_length=10)
    fecha = models.DateField()
    nombre_reloj = models.CharField(max_length=100)
    id_reloj = models.CharField(max_length=20)
    persona = models.CharField(max_length=2)
    num_importacion = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gui_string

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'