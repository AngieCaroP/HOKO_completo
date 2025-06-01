from django import forms
from .models import Producto, Stock, Bodega, GuiaEnvio

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'bodega': forms.Select(attrs={'class': 'form-control'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'umbral_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bodega'].queryset = Bodega.objects.all().order_by('nombre')
        if 'estado' in self.fields:
            self.fields['estado'].disabled = True

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'direccion', 'telefono', 'ciudad'] # AÑADIR 'ciudad'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}), # Widget para ciudad
            # Si usaste choices en el modelo para ciudad:
            # 'ciudad': forms.Select(attrs={'class': 'form-control'}),
        }

class GuiaEnvioForm(forms.ModelForm):
    class Meta:
        model = GuiaEnvio
        fields = [
            'cliente_nombre', 'cliente_telefono', 'cliente_ciudad',
            'cliente_direccion', 'cliente_direccion2',
            'producto',         # <--- AÑADIR ESTO
            'cantidad',         # <--- AÑADIR ESTO
            'contenido_resumen',
            'observaciones', 'estado',
        ]
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente_ciudad': forms.Select(attrs={'class': 'form-control'}),
            'cliente_direccion': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'cliente_direccion2': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'contenido_resumen': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_contenido'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'estado' in self.fields:
             self.fields['estado'].initial = 'pendiente'
        if 'cliente_ciudad' in self.fields:
            self.fields['cliente_ciudad'].choices = sorted(GuiaEnvio.CIUDAD_CHOICES, key=lambda x: x[1])
            self.fields['cliente_ciudad'].required = True

        self.fields['cliente_nombre'].required = True
        self.fields['cliente_telefono'].required = True
        self.fields['cliente_direccion'].required = True