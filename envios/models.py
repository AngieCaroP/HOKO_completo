#envios/models.py
# envios/models.py
from django.db import models
from decimal import Decimal
from django.urls import reverse
from django.utils import timezone # Import timezone

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
    ciudad = models.CharField(max_length=100, blank=True, null=True) # ASEGÚRATE DE QUE ESTÁ AQUÍ

    def __str__(self):
        return f"{self.nombre} ({self.ciudad or 'Ciudad no especificada'})"
# ...

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
        # Add more cities as needed
  
    ]

    cliente_nombre = models.CharField(max_length=100)
    cliente_telefono = models.CharField(max_length=20)
    cliente_ciudad = models.CharField(max_length=50, choices=CIUDAD_CHOICES, verbose_name='Ciudad')
    cliente_direccion = models.TextField()
    cliente_direccion2 = models.TextField(blank=True, null=True)

    # These fields (producto, cantidad) might become redundant if items_guia is always used.
    # For now, they are kept as per your view logic, but you might reconsider their necessity.
    producto = models.ForeignKey(
        Producto,
        on_delete=models.PROTECT, # Or SET_NULL if a product can be deleted but guias remain
        related_name='guias_como_principal',
        null=True, blank=True, # Allow them to be blank if items_guia handles this
        verbose_name="Producto Principal (Ref.)"
    )
    cantidad = models.PositiveIntegerField(
        default=1, null=True, blank=True, # Allow blank
        verbose_name="Cantidad Principal (Ref.)"
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
        
        # Logic to update contenido_resumen based on items_guia
        # This should happen *before* saving if items_guia are managed separately
        # or after saving if items_guia are saved in the same transaction and then this is updated.
        # For now, let's assume contenido_resumen is set in the form/view.

        super().save(*args, **kwargs) # Save first to get an ID if it's new

        if is_new and not self.codigo_seguimiento:
            # Generate code only after the first save guarantees an ID
            self.codigo_seguimiento = f"HOKO-{self.id:05d}"
            # Save again just to update the code, avoiding recursion
            super().save(update_fields=['codigo_seguimiento'])

    @property
    def total_guia(self):
        if hasattr(self, 'items_guia') and self.items_guia.exists():
            return sum(item.subtotal for item in self.items_guia.all())
        return Decimal('0.00')

class GuiaEnvioProducto(models.Model):
    guia_envio = models.ForeignKey(GuiaEnvio, related_name='items_guia', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT) # PROTECT or handle deletion
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario_en_guia = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto al momento de crear la guía")

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario_en_guia

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Guía #{self.guia_envio_id if self.guia_envio_id else 'Nueva'}"

    class Meta:
        unique_together = ('guia_envio', 'producto')
        verbose_name = "Producto en Guía de Envío"
        verbose_name_plural = "Productos en Guías de Envío"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update GuiaEnvio's contenido_resumen and potentially producto/cantidad (if you want to keep them synced)
        if self.guia_envio:
            items = self.guia_envio.items_guia.all()
            resumen_parts = []
            if items:
                for item in items:
                    resumen_parts.append(f"{item.cantidad}x {item.producto.nombre}")
                
                # Update producto and cantidad fields of GuiaEnvio with the first item
                # This is based on your view logic.
                first_item = items.first()
                self.guia_envio.producto = first_item.producto
                self.guia_envio.cantidad = first_item.cantidad
                self.guia_envio.contenido_resumen = ", ".join(resumen_parts)
            else:
                self.guia_envio.producto = None
                self.guia_envio.cantidad = 0
                self.guia_envio.contenido_resumen = ""
            
            self.guia_envio.save(update_fields=['producto', 'cantidad', 'contenido_resumen'])


class Campaign(models.Model):
    gui_string = models.CharField(max_length=255, unique=True)
    pais = models.CharField(max_length=3) # e.g., COL, ECU
    plataforma = models.CharField(max_length=10) # e.g., F (Facebook), T (TikTok) -> adjusted max_length
    tipo_campana = models.CharField(max_length=10) # e.g., CBO, ABO
    fecha = models.DateField(default=timezone.now) # Use timezone.now for default
    nombre_reloj = models.CharField(max_length=100)
    id_reloj = models.CharField(max_length=20, blank=True, null=True) # ID might not always be present
    persona = models.CharField(max_length=10) # e.g., DP, AC -> adjusted max_length
    num_importacion = models.CharField(max_length=20, blank=True, null=True) # adjusted max_length
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gui_string

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'