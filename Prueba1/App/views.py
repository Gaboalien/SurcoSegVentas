from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.models import User
from .models import Cliente, RolUsuario
from .forms import ClienteForm,GestionForm
from django.shortcuts import render, get_object_or_404



@login_required
def home(request):
    # Obtener el rol del usuario actual
    rol_usuario = None
    try:
        rol_usuario = RolUsuario.objects.get(usuario=request.user)
    except RolUsuario.DoesNotExist:
        pass

    # Si es supervisor, ver todos los clientes; si no, solo los suyos
    if rol_usuario and rol_usuario.rol == 'supervisor':
        clientes = Cliente.objects.all().order_by('-cliente_desde')
    else:
        clientes = Cliente.objects.filter(usuario=request.user).order_by('-cliente_desde')

    # Filtro por resultado reciente si se envía
    filtro_resultado = request.GET.get('resultado')

    if filtro_resultado:
        if filtro_resultado == "Sin gestión":
            clientes = [c for c in clientes if not c.gestiones.exists()]
        else:
            clientes = [
                c for c in clientes
                if (ultima := c.gestiones.order_by('-fecha').first()) and
                   ultima.resultado == filtro_resultado
            ]

    # Agregar el resultado legible como atributo temporal
    for cliente in clientes:
        ultima_gestion = cliente.gestiones.order_by('-fecha').first()
        cliente.ultimo_resultado = (
            ultima_gestion.get_resultado_display() if ultima_gestion else "Sin gestión"
        )

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


@login_required
def supervisores_view(request):
    try:
        rol_usuario = RolUsuario.objects.get(usuario=request.user)
        if rol_usuario.rol != 'supervisor':
            return redirect('home')
    except RolUsuario.DoesNotExist:
        return redirect('home')

    filtro_resultado = request.GET.get('resultado')
    filtro_agente = request.GET.get('agente')

    # Obtener todos los agentes (usuarios distintos al actual supervisor)
    agentes = User.objects.exclude(id=request.user.id)

    clientes_qs = Cliente.objects.all().order_by('-cliente_desde')

    # Aplicar filtro por agente
    if filtro_agente:
        clientes_qs = clientes_qs.filter(usuario_id=filtro_agente)

    clientes_filtrados = []
    for cliente in clientes_qs:
        ultima_gestion = cliente.gestiones.order_by('-fecha').first()

        if filtro_resultado:
            if filtro_resultado == "Sin gestión" and not ultima_gestion:
                clientes_filtrados.append(cliente)
            elif ultima_gestion and ultima_gestion.resultado == filtro_resultado:
                clientes_filtrados.append(cliente)
        else:
            clientes_filtrados.append(cliente)

        cliente.ultimo_resultado = (
            ultima_gestion.get_resultado_display() if ultima_gestion else "Sin gestión"
        )

    form = ClienteForm()

    return render(request, 'supervisores.html', {
        'clientes': clientes_filtrados,
        'form': form,
        'rol_usuario': rol_usuario,
        'filtro_resultado': filtro_resultado,
        'filtro_agente': filtro_agente,
        'agentes': agentes
    })

def parse_fecha(valor):
    if not valor or valor == "":
        return None
    try:
        return datetime.strptime(valor, "%Y-%m-%d").date()
    except ValueError:
        return None


@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    rol = RolUsuario.objects.filter(usuario=request.user).first()

    if rol is None or (rol.rol != 'supervisor' and cliente.usuario != request.user):
        return redirect('home')

    gestiones = cliente.gestiones.order_by('-fecha')

    if request.method == 'POST':
        if 'resultado' in request.POST:
            form = GestionForm(request.POST, cliente=cliente)
            if form.is_valid():
                gestion = form.save(commit=False)
                gestion.cliente = cliente

                resultado = gestion.resultado
                surco_opcion = form.cleaned_data.get('surco_opcion')
                

                if resultado == 'venta':
                    if surco_opcion == 'vida':
                        cliente.surco_vida = 'Sí'
                        gestion.poliza = "110316"
                        gestion.domicilio_calle = "ITUZAINGÓ"
                        gestion.domicilio_numero = "1315"
                        gestion.domicilio_apto = "0"
                        gestion.departamento = "MONTEVIDEO"
                        gestion.localidad = "MONTEVIDEO"
                        gestion.telefono = "18918"  # Asigna el número elegido
                        gestion.mes_pago = form.cleaned_data.get('mes_pago')
                        gestion.telefono_venta = form.cleaned_data.get('telefono_venta')
                elif surco_opcion == 'hogar':
                        cliente.surco_hogar = 'Sí'

                        # Campos vacíos para Surco Hogar
                        gestion.poliza = None
                        gestion.domicilio_calle = None
                        gestion.domicilio_numero = None
                        gestion.domicilio_apto = None
                        gestion.departamento = None
                        gestion.localidad = None
                        gestion.telefono = None
                        gestion.mes_pago = None

                        # Datos del formulario
                        gestion.telefono_venta = form.cleaned_data.get('telefono_venta')
                        gestion.email_venta = form.cleaned_data.get('email_venta')

                        gestion.seguridad = form.cleaned_data.get('seguridad')
                        gestion.paredes = form.cleaned_data.get('paredes')
                        gestion.techo = form.cleaned_data.get('techo')
                        gestion.inmueble = form.cleaned_data.get('inmueble')
                        gestion.vivienda = form.cleaned_data.get('vivienda')
                else:
                    # No es venta, limpiar todos los campos
                    gestion.poliza = None
                    gestion.domicilio_calle = None
                    gestion.domicilio_numero = None
                    gestion.domicilio_apto = None
                    gestion.departamento = None
                    gestion.localidad = None
                    gestion.telefono = None
                    gestion.mes_pago = None
                    gestion.telefono_venta = None

                gestion.save()
                cliente.save()
                return redirect('detalle_cliente', cliente_id=cliente.id)
        else:
            campos_editables = [
                'cliced_a', 'tarven', 'cliapeuno', 'cliapedos', 'clinomuno', 'clinomdos',
                'clifecnac', 'loc', 'dpto', 'clical', 'clindp', 'clibis', 'clirut', 'clikms',
                'clipas', 'cliblo', 'clitor', 'cliapt', 'climan', 'telp', 'telt', 'cel1',
                'cel2', 'telbau', 'telweb', 'celweb', 'email', 'genero', 'surco_vida', 'surco_hogar'
            ]
            for campo in campos_editables:
                nuevo_valor = request.POST.get(campo)
                if campo == 'clifecnac':
                    cliente.clifecnac = parse_fecha(nuevo_valor)
                else:
                    setattr(cliente, campo, nuevo_valor if nuevo_valor != "" else None)

            cliente.save()
            return redirect('detalle_cliente', cliente_id=cliente.id)
    else:
        form = GestionForm(cliente=cliente)

    return render(request, 'detalle_cliente.html', {
        'cliente': cliente,
        'gestiones': gestiones,
        'form': form
    })

