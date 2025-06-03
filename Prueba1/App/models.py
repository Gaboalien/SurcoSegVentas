from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)  # Clave primaria autoincremental

    cuenro_a = models.CharField(max_length=20, null=True, blank=True)
    cliced_a = models.CharField(max_length=20, null=True, blank=True)
    rescierre = models.DateField(null=True, blank=True)
    resvto = models.DateField(null=True, blank=True)
    cliente_desde = models.DateField(null=True, blank=True)
    tarven = models.DateField(null=True, blank=True)
    cliapeuno = models.CharField(max_length=100, null=True, blank=True)
    cliapedos = models.CharField(max_length=100, null=True, blank=True)
    clinomuno = models.CharField(max_length=100, null=True, blank=True)
    clinomdos = models.CharField(max_length=100, null=True, blank=True)
    telt = models.CharField(max_length=20, null=True, blank=True)
    cel1 = models.CharField(max_length=20, null=True, blank=True)
    cel2 = models.CharField(max_length=20, null=True, blank=True)
    telbau = models.CharField(max_length=20, null=True, blank=True)
    telweb = models.CharField(max_length=20, null=True, blank=True)
    celweb = models.CharField(max_length=20, null=True, blank=True)
    surco_vida = models.CharField(max_length=50, null=True, blank=True)
    surco_hogar = models.CharField(max_length=50, null=True, blank=True)
    hasta = models.DateField(null=True, blank=True)

    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='clientes_cargados')
    fecha_carga = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.cliapeuno} {self.cliapedos}, {self.clinomuno} {self.clinomdos}"

class Gestion(models.Model):
    id = models.AutoField(primary_key=True)

    cliente = models.ForeignKey(
        Cliente,
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
    comentario = models.TextField(null=True, blank=True)  # 👈 nuevo campo
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
