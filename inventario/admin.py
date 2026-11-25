from django.contrib import admin

from .models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["nombre", "color", "cantidad"]
    search_fields = ["nombre", "color"]
    list_filter = ["nombre"]


admin.site.site_header = "Taller VHAJ"
admin.site.register(Material, MaterialAdmin)
