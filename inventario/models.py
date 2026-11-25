from django.db import models


class Material(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "materiales"

    def __str__(self):
        return f"{self.nombre} {self.color}"
