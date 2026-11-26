from django.contrib import admin

from .models import Pedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ["cliente", "pieza", "material", "cantidad", "fecha"]
    search_fields = ["cliente", "pieza", "material__nombre"]
    list_filter = ["fecha", "material__nombre"]
    readonly_fields = ["fecha"]


admin.site.register(Pedido, PedidoAdmin)
