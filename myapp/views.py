from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from .models import Cliente, TipoTarjeta, Tarjeta, TodoItem
from .forms import RegistroUserForm, ClienteForm, TipoTarjetaForm, TarjetaForm
from django.contrib.auth import get_user_model  # Importar get_user_model
from django.db import IntegrityError


# Página de inicio
def home(request):
    return render(request, "home.html")

# Vista protegida por login que muestra todos los elementos
@login_required
def todos(request):
    usuario = request.session.get("usuario", "cpazro")
    items = TodoItem.objects.all()
    return render(request, "todos.html", {"todos": items, "usuario": usuario})

# Registro de usuario con email

def registro_user(request):
    if request.method == 'POST':
        form = RegistroUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)  # No guarda el usuario todavía
                user.username = form.cleaned_data['email']  # Usa el email como nombre de usuario
                user.save()  # Guarda el usuario

                # Asegúrate de especificar el backend
                backend = 'myapp.backends.EmailBackend'  # Cambia a la ruta correcta si es necesario
                user.backend = backend  # Establece el backend
                login(request, user)  # Iniciar sesión automáticamente después de registrar

                # Almacenar el nombre en la sesión
                request.session['nombre_usuario'] = form.cleaned_data['nombre']  # Almacena el nombre en la sesión

                return redirect('dashboard_cliente')  # Redirigir a la página del dashboard
            except IntegrityError:
                form.add_error('email', 'Este correo electrónico ya ha sido registrado en otra cuenta.')
        else:
            print(form.errors)
    else:
        form = RegistroUserForm()

    return render(request, 'registro_user.html', {'form': form})



# Vista protegida para el carrito
@login_required
def carrito(request):
    return render(request, "carrito.html")

# Inicio de sesión
def inicio(request):
    return render(request, "inicio.html")

def despliegue(request):
    return render(request, "despliegue_producto.html")

def formulario(request):
    return render(request, "formulario_producto.html")

@login_required
def dashboard_cliente(request):
    nombre_usuario = request.session.get("nombre_usuario", "Usuario").capitalize()  # Obtiene el nombre de la sesión
    return render(request, "dashboard_cliente.html", {"usuario": nombre_usuario})



# Vista para listar clientes (solo para superusuarios)
@user_passes_test(lambda u: u.is_superuser)
def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_clientes.html', {'clientes': clientes})

# Vista para listar tarjetas
@user_passes_test(lambda u: u.is_superuser)
def lista_tarjeta(request):
    tarjetas = Tarjeta.objects.select_related('tipo', 'cliente').all()
    return render(request, 'lista_tarjeta.html', {'tarjetas': tarjetas})

# Vista para listar tipos de tarjeta
@user_passes_test(lambda u: u.is_superuser)
def lista_tipo_tarjeta(request):
    tipos_tarjeta = TipoTarjeta.objects.all()
    return render(request, 'lista_tipo_tarjeta.html', {'tipos_tarjeta': tipos_tarjeta})

# Vista para añadir Cliente
@login_required
def add_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'add_cliente.html', {'form': form})

# Vista para añadir TipoTarjeta
@login_required
def add_tipo_tarjeta(request):
    if request.method == 'POST':
        form = TipoTarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_tarjeta')
    else:
        form = TipoTarjetaForm()
    return render(request, 'add_tipo_tarjeta.html', {'form': form})

# Vista para añadir Tarjeta
@login_required
def add_tarjeta(request):
    if request.method == 'POST':
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tarjeta')
    else:
        form = TarjetaForm()
    return render(request, 'add_tarjeta.html', {'form': form})

# Vista para editar Cliente
@login_required
def edit_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_cliente.html', {'form': form})

# Vista para editar TipoTarjeta
@login_required
def edit_tipo_tarjeta(request, id_tipo):
    tipo_tarjeta = get_object_or_404(TipoTarjeta, id_tipo=id_tipo)
    if request.method == 'POST':
        form = TipoTarjetaForm(request.POST, instance=tipo_tarjeta)
        if form.is_valid():
            form.save()
            return redirect('lista_tipo_tarjeta')
    else:
        form = TipoTarjetaForm(instance=tipo_tarjeta)
    return render(request, 'edit_tipo_tarjeta.html', {'form': form})

# Vista para editar Tarjeta
@login_required
def edit_tarjeta(request, numero_tarjeta):
    tarjeta = get_object_or_404(Tarjeta, numero_tarjeta=numero_tarjeta)
    if request.method == 'POST':
        form = TarjetaForm(request.POST, instance=tarjeta)
        if form.is_valid():
            form.save()
            return redirect('lista_tarjeta')
    else:
        form = TarjetaForm(instance=tarjeta)
    return render(request, 'edit_tarjeta.html', {'form': form})

# Vista para eliminar Cliente
@login_required
def delete_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, 'delete_cliente.html', {'cliente': cliente})

# Vista para eliminar TipoTarjeta
@login_required
def delete_tipo_tarjeta(request, id_tipo):
    tipo_tarjeta = get_object_or_404(TipoTarjeta, id_tipo=id_tipo)
    if request.method == 'POST':
        tipo_tarjeta.delete()
        return redirect('lista_tipo_tarjeta')
    return render(request, 'delete_tipo_tarjeta.html', {'tipo_tarjeta': tipo_tarjeta})

# Vista para eliminar Tarjeta
@login_required
def delete_tarjeta(request, numero_tarjeta):
    tarjeta = get_object_or_404(Tarjeta, numero_tarjeta=numero_tarjeta)
    if request.method == 'POST':
        tarjeta.delete()
        return redirect('lista_tarjeta')
    return render(request, 'delete_tarjeta.html', {'tarjeta': tarjeta})
