from django.shortcuts import render

from .models import Pedido


def inicio(request):
    lista = Pedido.objects.order_by("-fecha")
    contexto = {"titulo": "Pedidos del taller", "pedidos": lista}

    return render(request, "pedidos/inicio.html", contexto)
