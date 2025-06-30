from django import forms
from .models import Cliente,Gestion

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'cliced_a', 'rescierre', 'resvto', 'cliente_desde', 'tarven',
            'cliapeuno', 'cliapedos', 'clinomuno', 'clinomdos', 'edad', 'clifecnac',
            'loc', 'dpto', 'clical', 'clindp', 'clibis', 'clirut', 'clikms', 'clipas',
            'cliblo', 'clitor', 'cliapt', 'climan', 'telp', 'telt', 'cel1', 'cel2',
            'telbau', 'telweb', 'celweb', 'surco_vida', 'surco_hogar', 'hasta',
            'fecha_carga', 'email', 'genero'
        ]
        labels = {
            'cliced_a': 'Cédula',
            'rescierre': 'Rescierre',
            'resvto': 'Resvto',
            'cliente_desde': 'Cliente desde',
            'tarven': 'Tarven',
            'cliapeuno': 'Apellido 1',
            'cliapedos': 'Apellido 2',
            'clinomuno': 'Nombre 1',
            'clinomdos': 'Nombre 2',
            'edad': 'Edad',
            'clifecnac': 'Fecha de nacimiento',
            'loc': 'Localidad',
            'dpto': 'Departamento',
            'clical': 'Calle',
            'clindp': 'Número de puerta',
            'clibis': 'Bis',
            'clirut': 'RUT',
            'clikms': 'Kms',
            'clipas': 'Paso',
            'cliblo': 'Bloque',
            'clitor': 'Torre',
            'cliapt': 'Apartamento',
            'climan': 'Manzana',
            'telp': 'Teléfono particular',
            'telt': 'Teléfono fijo',
            'cel1': 'Celular 1',
            'cel2': 'Celular 2',
            'telbau': 'Teléfono BAU',
            'telweb': 'Teléfono Web',
            'celweb': 'Celular Web',
            'surco_vida': 'Surco Vida',
            'surco_hogar': 'Surco Hogar',
            'hasta': 'Hasta',
            'fecha_carga': 'Fecha de carga',
            'email': 'Correo electrónico',
            'genero': 'Género',
        }

class GestionForm(forms.ModelForm):
    surco_opcion = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    telefono_venta = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2',
            'id': 'telefono-venta'
        }),
        label="Teléfono de Venta"
    )

    email_venta = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2',
            'id': 'email-venta'
        }),
        label="Email de Venta"
    )

    mes_pago = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2',
            'placeholder': 'Ej: Junio 2025'
        }),
        label="Mes de pago"
    )

    # Campos fijos para Surco Hogar
    seguridad = forms.CharField(
        required=False,
        initial="NO",
        widget=forms.HiddenInput()
    )

    paredes = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.HiddenInput()
    )

    techo = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.HiddenInput()
    )

    inmueble = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.HiddenInput()
    )

    vivienda = forms.CharField(
        required=False,
        initial="S",
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)

        if cliente:
            # Teléfonos
            opciones_tel = []
            campos_telefono = [
                ('telp', 'Tel. particular'),
                ('telt', 'Tel. fijo'),
                ('cel1', 'Celular 1'),
                ('cel2', 'Celular 2'),
                ('telbau', 'Tel. BAU'),
                ('telweb', 'Tel. Web'),
                ('celweb', 'Cel. Web'),
            ]
            for campo, label in campos_telefono:
                valor = getattr(cliente, campo, None)
                if valor and str(valor).lower() not in ['0', 'nan', '', 'none']:
                    opciones_tel.append((valor, f"{label}: {valor}"))
            if not opciones_tel:
                opciones_tel = [('', 'No disponible')]
            self.fields['telefono_venta'].choices = opciones_tel

            # Emails
            opciones_mail = []
            campos_email = ['email', 'email_alt', 'email_web']
            for campo in campos_email:
                valor = getattr(cliente, campo, None)
                if valor and str(valor).lower() not in ['nan', '', 'none']:
                    opciones_mail.append((valor, valor))
            if not opciones_mail:
                opciones_mail = [('', 'No disponible')]
            self.fields['email_venta'].choices = opciones_mail

    class Meta:
        model = Gestion
        fields = [
            'resultado', 'comentario', 'telefono_venta', 'email_venta', 'mes_pago',
            'seguridad', 'paredes', 'techo', 'inmueble', 'vivienda'
        ]
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