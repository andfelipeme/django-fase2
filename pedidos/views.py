from django.shortcuts import render


def inicio(request):
    lista = [
        {"cliente": "Pepito", "pieza": "00012.stl", "cantidad": 1},
        {"cliente": "Pepito G", "pieza": "00014.stl", "cantidad": 2},
        {"cliente": "Pepito R", "pieza": "00022.stl", "cantidad": 3},
    ]
    contexto = {"titulo": "Pedidos del taller", "pedidos": lista}

    return render(request, "pedidos/inicio.html", contexto)
