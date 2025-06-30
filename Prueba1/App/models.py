from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)

    cliced_a = models.CharField(max_length=100, blank=True, null=True)
    rescierre = models.CharField(max_length=100, blank=True, null=True)
    resvto = models.CharField(max_length=100, blank=True, null=True)
    cliente_desde = models.DateField(blank=True, null=True)
    tarven = models.CharField(max_length=100, blank=True, null=True)
    cliapeuno = models.CharField(max_length=100, blank=True, null=True)
    cliapedos = models.CharField(max_length=100, blank=True, null=True)
    clinomuno = models.CharField(max_length=100, blank=True, null=True)
    clinomdos = models.CharField(max_length=100, blank=True, null=True)
    edad = models.PositiveIntegerField(blank=True, null=True)
    clifecnac = models.DateField(blank=True, null=True)
    loc = models.CharField(max_length=100, blank=True, null=True)
    dpto = models.CharField(max_length=100, blank=True, null=True)
    clical = models.CharField(max_length=100, blank=True, null=True)
    clindp = models.CharField(max_length=100, blank=True, null=True)
    clibis = models.CharField(max_length=10, blank=True, null=True)
    clirut = models.CharField(max_length=50, blank=True, null=True)
    clikms = models.CharField(max_length=50, blank=True, null=True)
    clipas = models.CharField(max_length=50, blank=True, null=True)
    cliblo = models.CharField(max_length=50, blank=True, null=True)
    clitor = models.CharField(max_length=50, blank=True, null=True)
    cliapt = models.CharField(max_length=50, blank=True, null=True)
    climan = models.CharField(max_length=50, blank=True, null=True)
    telp = models.CharField(max_length=20, blank=True, null=True)
    telt = models.CharField(max_length=20, blank=True, null=True)
    cel1 = models.CharField(max_length=20, blank=True, null=True)
    cel2 = models.CharField(max_length=20, blank=True, null=True)
    telbau = models.CharField(max_length=20, blank=True, null=True)
    telweb = models.CharField(max_length=20, blank=True, null=True)
    celweb = models.CharField(max_length=20, blank=True, null=True)

    surco_vida = models.CharField(max_length=2, choices=[("Sí", "Sí"), ("No", "No")], default="No")
    surco_hogar = models.CharField(max_length=2, choices=[("Sí", "Sí"), ("No", "No")], default="No")
    hasta = models.DateField(blank=True, null=True)

    email = models.EmailField(blank=True, null=True)
    genero = models.CharField(
        max_length=20,
        choices=[
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino")
        ],
        default="No especificado",
        blank=True,
        null=True
    )
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes')
    fecha_carga = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.cliapeuno} {self.cliapedos}, {self.clinomuno} {self.clinomdos}"

        

class Gestion(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        'Cliente',
        on_delete=models.CASCADE,
        related_name='gestiones'
    )

    RESULTADO_CHOICES = [
        ('venta', 'Venta'),
        ('rechazo', 'Rechazo'),
        ('pendiente', 'Pendiente'),
        ('rellamar', 'Rellamar'),
        ('llamar_mañana', 'Llamar de mañana'),
        ('llamar_tarde', 'Llamar de tarde'),
        ('llamar_sabado', 'Llamar sábado'),
        ('no_target', 'No target'),
        ('dato_erroneo', 'Dato erróneo'),
    ]

    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    comentario = models.TextField(null=True, blank=True)
    telefono_venta = models.CharField(max_length=20, blank=True, null=True)
    mes_pago = models.CharField(max_length=20, blank=True, null=True)

    # Campos que solo deben llenarse manualmente en Surco Vida (sin default)
    poliza = models.CharField(max_length=20, blank=True, null=True)
    domicilio_calle = models.CharField(max_length=100, blank=True, null=True)
    domicilio_numero = models.CharField(max_length=10, blank=True, null=True)
    domicilio_apto = models.CharField(max_length=10, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    localidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email_venta = models.EmailField(blank=True, null=True)
    seguridad = models.CharField(max_length=10, blank=True, null=True)  # Ej: 'NO'
    paredes = models.IntegerField(blank=True, null=True)  # Ej: 1
    techo = models.IntegerField(blank=True, null=True)  # Ej: 1
    inmueble = models.IntegerField(blank=True, null=True)  # Ej: 1
    vivienda = models.CharField(max_length=10, blank=True, null=True)  # Ej: 'S'

    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gestión del cliente {self.cliente_id} - {self.resultado} ({self.fecha.strftime('%Y-%m-%d %H:%M')})"


        
class RolUsuario(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('supervisor', 'Supervisor'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_rol_display()}"
