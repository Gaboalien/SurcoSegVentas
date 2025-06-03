from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Cliente, RolUsuario
from .forms import ClienteForm,GestionForm
from django.shortcuts import render, get_object_or_404


@login_required
def home(request):
    clientes = Cliente.objects.filter(usuario=request.user).order_by('-fecha_carga')

    # Filtro por resultado reciente si se envía
    filtro_resultado = request.GET.get('resultado')
    if filtro_resultado:
        clientes = [c for c in clientes if c.gestiones.order_by('-fecha').first() and c.gestiones.order_by('-fecha').first().resultado == filtro_resultado]

    # Agregar el último resultado como atributo temporal
    for cliente in clientes:
        ultima_gestion = cliente.gestiones.order_by('-fecha').first()
        cliente.ultimo_resultado = ultima_gestion.resultado if ultima_gestion else "Sin gestión"

    rol_usuario = None
    try:
        rol_usuario = RolUsuario.objects.get(usuario=request.user)
    except RolUsuario.DoesNotExist:
        pass

    form = ClienteForm()

    return render(request, 'home.html', {
        'clientes': clientes,
        'form': form,
        'rol_usuario': rol_usuario,
        'filtro_resultado': filtro_resultado
    })


# Función para salir de la sesión
def salir(request):
    logout(request)
    return redirect('/')


# Vista de login personalizada con redirección por rol
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            try:
                rol_usuario = RolUsuario.objects.get(usuario=user)
                if rol_usuario.rol == 'administrador':
                    return redirect('home')
                elif rol_usuario.rol == 'supervisor':
                    return redirect('supervisores')
                else:
                    return redirect('home')
            except RolUsuario.DoesNotExist:
                return render(request, 'registration/login.html', {'error': 'Rol de usuario no encontrado.'})
        else:
            return render(request, 'registration/login.html', {'error': 'Credenciales inválidas. Intenta de nuevo.'})

    return render(request, 'registration/login.html')


# Vista para supervisores
@login_required
def supervisores_view(request):
    return render(request, 'supervisores.html')

@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id, usuario=request.user)
    gestiones = cliente.gestiones.order_by('-fecha')  # Obtener gestiones del cliente

    if request.method == 'POST':
        form = GestionForm(request.POST)
        if form.is_valid():
            gestion = form.save(commit=False)
            gestion.cliente = cliente
            gestion.save()

            # Verificar si se eligió 'venta' y hay una opción de surco
            surco_opcion = form.cleaned_data.get('surco_opcion')
            if gestion.resultado == 'venta' and surco_opcion:
                if surco_opcion == 'vida':
                    cliente.surco_vida = 'Sí'
                elif surco_opcion == 'hogar':
                    cliente.surco_hogar = 'Sí'
                cliente.save()

            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = GestionForm()

    return render(request, 'detalle_cliente.html', {
        'cliente': cliente,
        'gestiones': gestiones,
        'form': form
    })
    