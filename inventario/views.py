from django.shortcuts import render

from .models import Material


def inicio(request):
    contexto = {"titulo": "Inventario de Taller VHAJ"}

    return render(request, "inventario/inicio.html", contexto)


def materiales(request):
    lista = Material.objects.order_by("nombre", "color")
    contexto = {"titulo": "Materiales del taller", "materiales": lista}

    return render(request, "inventario/materiales.html", contexto)
