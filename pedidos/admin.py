from django.contrib import admin

from .models import Pedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ["cliente", "pieza", "cantidad", "fecha"]
    search_fields = ["cliente", "pieza"]
    list_filter = ["fecha"]
    readonly_fields = ["fecha"]


admin.site.register(Pedido, PedidoAdmin)
