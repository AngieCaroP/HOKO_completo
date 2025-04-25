from django import forms
from .models import GuiaEnvio, Producto, Stock, Bodega, Transportadora

class GuiaEnvioForm(forms.ModelForm):
    class Meta:
        model = GuiaEnvio
        fields = '__all__'
        exclude = ['numero_guia', 'fecha_creacion', 'fecha_actualizacion']
        widgets = {
            'cliente_direccion': forms.Textarea(attrs={'rows': 3}),
            'contenido': forms.TextInput(attrs={'maxlength': '39'}),
        }

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

class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class TransportadoraForm(forms.ModelForm):
    class Meta:
        model = Transportadora
        fields = '__all__'