from django.contrib import admin
from .models import Cliente, Gestion, RolUsuario

# Admin para Cliente
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cliced_a', 'cliapeuno', 'cliapedos', 'clinomuno', 'usuario', 'fecha_carga')
    search_fields = ('cliced_a', 'cliapeuno', 'clinomuno', 'cel1', 'cel2')
    list_filter = ('fecha_carga', 'usuario')
    ordering = ('-fecha_carga',)

# Admin para Gestion
class GestionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'resultado', 'fecha')
    search_fields = ('cliente__cliced_a', 'resultado')
    list_filter = ('resultado', 'fecha')
    ordering = ('-fecha',)

# Admin para RolUsuario (ya estaba bien)
class RolUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol')
    search_fields = ('usuario__username', 'rol')
    list_filter = ('rol',)
    ordering = ('usuario',)



# Registro de modelos
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Gestion, GestionAdmin)
admin.site.register(RolUsuario, RolUsuarioAdmin)
