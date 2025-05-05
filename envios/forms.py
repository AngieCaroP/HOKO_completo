from django import forms
from .models import  Producto, Stock, Bodega, GuiaEnvio  # Asegúrate de importar Bodega de models.py

#producto
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

#stock
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
        # Asegúrate que el queryset de bodegas esté ordenado
        self.fields['bodega'].queryset = Bodega.objects.all().order_by('nombre')
        
#bodegas
class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'direccion', 'telefono']

#guias

# envios/forms.py (actualización)

class GuiaEnvioForm(forms.ModelForm):
    class Meta:
        model = GuiaEnvio
        fields = '__all__'
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'cliente_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'cliente_ciudad': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'cliente_direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'required': 'required'
            }),
             'cliente_direccion2': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'required': 'required'
            }),
            'producto': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'min': 1
            }),
        }
        model = GuiaEnvio
        fields = '__all__'
        widgets = {
            'cliente_ciudad': forms.Select(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valor por defecto para estado
        self.fields['estado'].initial = 'pendiente'
        # Ordenar productos por nombre
        self.fields['producto'].queryset = Producto.objects.order_by('nombre')
        # Configurar campos requeridos
        self.fields['cliente_nombre'].required = True
        self.fields['cliente_telefono'].required = True
        self.fields['cliente_ciudad'].required = True
        self.fields['cliente_direccion'].required = True
        self.fields['producto'].required = True
        self.fields['cantidad'].required = True
        # Ordenar las ciudades alfabéticamente
        self.fields['cliente_ciudad'].choices = sorted(GuiaEnvio.CIUDAD_CHOICES, key=lambda x: x[1])