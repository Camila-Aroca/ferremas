from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db import connection
from .models import Cliente, TipoTarjeta, Tarjeta, TodoItem, Producto, Categoria, Carrito, CarritoProducto
from .forms import RegistroUserForm, ClienteForm, TipoTarjetaForm, TarjetaForm
from django.contrib.auth import get_user_model  # Importar get_user_model
from django.db import IntegrityError
import unicodedata


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

def despliegue_producto(request, sku):
    # Obtener el producto específico usando get_object_or_404 para manejar errores
    producto = get_object_or_404(Producto, sku=sku)  # Cambiado a sku

    context = {
        'producto': producto,
    }

    return render(request, 'despliegue_producto.html', context)

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

def normalize_string(text):
    """Elimina los acentos y normaliza la cadena"""
    return ''.join(
        c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c)
    )

def catalogo(request):
    # Filtramos los productos como QuerySet desde el principio
    productos = Producto.objects.all()

    # Capturar el filtro de categoría
    categoria = request.GET.get('categoria')
    if categoria:
        productos = productos.filter(categoria__nombre=categoria)

    # Capturar el filtro de marca
    marca = request.GET.get('marca')
    if marca:
        productos = productos.filter(marca=marca)

    # Capturar la consulta de búsqueda del usuario
    query = request.GET.get('q')
    if query:
        # Normalizar la consulta
        query_normalized = normalize_string(query.lower())

        # Convertir productos a lista y filtrar en Python
        productos = [
            producto for producto in productos
            if query_normalized in normalize_string(producto.nombre.lower())
        ]

    # Pasar las categorías y marcas únicas al contexto
    context = {
        'productos': productos,
        'categorias': Categoria.objects.all(),
        'marcas': Producto.objects.values_list('marca', flat=True).distinct(),
    }

    return render(request, 'catalogo.html', context)

@login_required
def agregar_al_carrito(request, sku):
    producto = get_object_or_404(Producto, sku=sku)

    # Obtener o crear el carrito del usuario
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Agregar el producto al carrito
    carrito_producto, created = CarritoProducto.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )

    if not created:
        # Si ya existía, solo aumentar la cantidad
        carrito_producto.cantidad += 1
        carrito_producto.save()

    return redirect('carrito') 

@login_required
def carrito(request):
    # Obtiene el carrito del usuario actual
    carrito = Carrito.objects.filter(usuario=request.user).first()
    
    # Si el carrito existe, obtiene los productos y calcula el total
    if carrito:
        productos = carrito.carritoproducto_set.all()
        # Calcula el total sumando los subtotales de cada producto
        total = sum(item.producto.precio * item.cantidad for item in productos)
    else:
        productos = []
        total = 0

    # Pasa los productos y el total al template
    return render(request, "carrito.html", {"carrito": carrito, "productos": productos, "total": total})

@login_required
def eliminar_del_carrito(request, sku):
    # Intenta obtener el producto por SKU
    producto = get_object_or_404(Producto, sku=sku)
    
    # Obtiene el carrito del usuario actual
    carrito = Carrito.objects.filter(usuario=request.user).first()
    
    if carrito:
        # Intenta obtener el CarritoProducto asociado al producto
        carrito_producto = carrito.carritoproducto_set.filter(producto=producto).first()
        
        if carrito_producto:
            # Obtener la cantidad a eliminar del formulario
            cantidad_a_eliminar = int(request.POST.get('cantidad_a_eliminar', 1))

            # Verificar si la cantidad a eliminar es mayor que la cantidad en el carrito
            if cantidad_a_eliminar >= carrito_producto.cantidad:
                carrito_producto.delete()  # Elimina el producto del carrito si la cantidad es igual o mayor
            else:
                # Disminuir la cantidad en lugar de eliminar el producto
                carrito_producto.cantidad -= cantidad_a_eliminar
                carrito_producto.save()  # Guarda los cambios en el carrito
        else:
            return HttpResponse("Producto no encontrado en el carrito.", status=404)
    
    return redirect('carrito')

def compra_aprobada(request):
    return render(request, 'compra_aprobada.html')  # Ajusta el nombre si es necesario

def compra_fallida(request):
    return render(request, 'compra_fallida.html')  
