from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import catalogo
from .views import despliegue_producto
from .views import agregar_al_carrito
from .views import eliminar_del_carrito
from .views import compra_aprobada
from .views import compra_fallida

urlpatterns = [
    path("", views.inicio, name="home"),
    path("admin/", admin.site.urls),
    path("carrito/todos/", views.todos, name="todos"),
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/inicio/", views.inicio, name="inicio"),
    path("carrito/despliegue-producto/", views.despliegue_producto, name="despliegue-producto"),
    path("carrito/formulario-producto/", views.formulario, name="formulario-producto"),
    path("carrito/registro-user/", views.registro_user, name="registro-user"),
    path('carrito/login', views.login, name='login'),
    path("carrito/dashboard_cliente/", views.dashboard_cliente, name="dashboard_cliente"),
    
    path('carrito/clientes/', views.lista_clientes, name='lista_clientes'),
    path('carrito/tarjetas/', views.lista_tarjeta, name='lista_tarjeta'),
    path('carrito/tipos-tarjeta/', views.lista_tipo_tarjeta, name='lista_tipo_tarjeta'),

    path('carrito/add_cliente/', views.add_cliente, name='add_cliente'),
    path('carrito/add_tipo_tarjeta/', views.add_tipo_tarjeta, name='add_tipo_tarjeta'),
    path('carrito/add_tarjeta/', views.add_tarjeta, name='add_tarjeta'),

    path('carrito/edit_cliente/<int:id>/', views.edit_cliente, name='edit_cliente'),
    path('carrito/edit_tipo_tarjeta/<int:id_tipo>/', views.edit_tipo_tarjeta, name='edit_tipo_tarjeta'),
    path('carrito/edit_tarjeta/<str:numero_tarjeta>/', views.edit_tarjeta, name='edit_tarjeta'),

    path('carrito/delete_cliente/<int:id>/', views.delete_cliente, name='delete_cliente'),
    path('carrito/delete_tipo_tarjeta/<int:id_tipo>/', views.delete_tipo_tarjeta, name='delete_tipo_tarjeta'),
    path('carrito/delete_tarjeta/<str:numero_tarjeta>/', views.delete_tarjeta, name='delete_tarjeta'),
    
    path("carrito/catalogo/", views.catalogo, name="catalogo"),
    path("carrito/catalogo/<int:id_categoria>/", views.catalogo, name="catalogo_categoria"),

    path('carrito/despliegue-producto/<str:sku>/', despliegue_producto, name='despliegue_producto'),


    path('agregar-al-carrito/<str:sku>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/eliminar/<str:sku>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    path('carrito/compra_aprobada/', compra_aprobada, name='compra_aprobada'),
    path('carrito/compra_fallida/', compra_fallida, name='compra_fallida'),

    
]

# Añadir las siguientes líneas para manejar archivos multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
