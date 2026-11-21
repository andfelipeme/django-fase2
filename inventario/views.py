from django.shortcuts import render


# Create your views here.
def inicio(request):
    contexto = {"titulo": "Inventario de Taller VHAJ"}

    return render(request, "inventario/inicio.html", contexto)


def materiales(request):
    lista = [
        {"nombre": "PLA", "color": "Negro", "cantidad": 1000},
        {"nombre": "PETG", "color": "Blanco", "cantidad": 1000},
        {"nombre": "TPU", "color": "Rojo", "cantidad": 1000},
    ]
    contexto = {"titulo": "Materiales del taller", "materiales": lista}

    return render(request, "inventario/materiales.html", contexto)
