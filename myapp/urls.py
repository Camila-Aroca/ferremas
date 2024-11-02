from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path("", views.inicio, name="home"),
    path("admin/", admin.site.urls),
    path("carrito/todos/", views.todos, name="todos"),
    path("carrito/", views.carrito, name="carrito"),
    #path("carrito/inicio2/", views.inicio2, name="inicio2"),
    path("carrito/inicio/", views.inicio, name="inicio"),
    path("carrito/despliegue-producto/", views.despliegue, name="despliegue-producto"),
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
]

