from django import forms
from .models import  Producto, Stock, Bodega  # Asegúrate de importar Bodega de models.py

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
        self.fields['bodega'].queryset = Bodega.objects.filter(
            nombre__in=['GUAYAQUIL', 'QUITO']  # Filtra solo las bodegas específicas
        )

#bodegas
class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ['nombre', 'direccion', 'telefono']