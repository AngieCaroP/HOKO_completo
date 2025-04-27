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

class GuiaEnvioForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control select-producto',
            'id': 'producto-select'
        }),
        label="Producto"
    )
    
    class Meta:
        model = GuiaEnvio
        fields = '__all__'
        widgets = {
            'cliente_nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'cliente_telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0991234567'
            }),
            'cliente_ciudad': forms.Select(attrs={
                'class': 'form-control select-ciudad'
            }),
            'cliente_direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección principal'
            }),
              'cliente_direccion2': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección secundaria'
            }),
            'contenido': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '39'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Instrucciones especiales'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.order_by('nombre')