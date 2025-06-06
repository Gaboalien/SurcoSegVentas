"""
URL configuration for Prueba1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('salir/', views.salir, name="salir"),
    path('login/', views.login_view, name='login'),
    path('supervisores/', views.supervisores_view, name='supervisores'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente')
]
