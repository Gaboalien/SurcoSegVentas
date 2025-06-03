from django import forms
from .models import Cliente,Gestion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['cliapeuno', 'cliced_a', 'cel1']  # Campos que se mostrarán
        labels = {
            'cliapeuno': 'Apellido',
            'cliced_a': 'Cédula',
            'cel1': 'Teléfono',
        }

class GestionForm(forms.ModelForm):
    surco_opcion = forms.ChoiceField(
        choices=[
            ('vida', 'Surco Vida'),
            ('hogar', 'Surco Hogar'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2',
            'id': 'surco-opcion'
        })
    )

    class Meta:
        model = Gestion
        fields = ['resultado', 'comentario']
        widgets = {
            'resultado': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2',
                'id': 'resultado-select'
            }),
            'comentario': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2',
                'rows': 4
            }),
        }