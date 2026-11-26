# Fase 2: Modelos, ORM, migraciones y Django Admin

Verificado con Django 6.1.3, Python 3.15.2 y uv 0.13.9.

Gestor de inventario y pedidos para el taller de impresión 3D **VHAJ**. Este repositorio es la Fase 2 del curso de Django: los datos dejan de estar en listas de Python y pasan a una base de datos, con modelos, migraciones, el panel de administración, consultas con el ORM y una relación entre pedidos y materiales.

## Cómo ejecutar el proyecto

Necesitas [uv](https://docs.astral.sh/uv/). uv descarga Python 3.15 solo, según el archivo `.python-version`.

Después de clonar el repositorio, desde la carpeta `fase2`:

```bash
uv sync                              # crea el entorno e instala Django
uv run manage.py migrate             # crea la base de datos
uv run manage.py createsuperuser     # usuario para el admin
uv run manage.py runserver
```

`db.sqlite3` no está en el repositorio, así que la base de datos arranca vacía. Los materiales y los pedidos se crean desde el admin.

| Dirección | Qué muestra |
|---|---|
| `/inventario/` | Inicio del inventario |
| `/inventario/materiales/` | Materiales ordenados por nombre y color, con cuántos pedidos usa cada uno |
| `/pedidos/` | Pedidos del más reciente al más antiguo, con su material |
| `/admin/` | Panel de administración |

## Estructura

```
fase2/
├── config/        configuración del proyecto (settings.py, urls.py)
├── inventario/    app de materiales: modelo Material
├── pedidos/       app de pedidos: modelo Pedido, con ForeignKey a Material
├── templates/     base.html
└── manage.py
```

## Contenido

| Clase | Tema |
|---|---|
| 0 | Arrancar un proyecto Django desde cero |
| 1 | Modelos y migraciones |
| 2 | Django Admin |
| 3 | Consultas con el ORM |
| 4 | Relaciones entre modelos (`ForeignKey`) |

---

## Clase 0: Arrancar un proyecto Django desde cero

### Conceptos

| Concepto | Qué es y para qué sirve |
|---|---|
| `uv init --no-package` | Crea un proyecto simple de Python, sin sistema de build. Es el tipo de proyecto que sirve para Django. |
| `startproject config .` | Crea la configuración del proyecto en la carpeta `config/`. El punto evita una carpeta `config/config/` de más. |
| `startapp` | Crea una app: un módulo con una función concreta, como `inventario` o `pedidos`. |
| `INSTALLED_APPS` | La lista de apps activas. Django solo ve los modelos y los templates de las apps registradas. |
| `app_name` | El espacio de nombres de las URLs de una app. Permite escribir `{% url 'inventario:inicio' %}`. |
| `DIRS` | Las carpetas de templates del proyecto, como `templates/`, donde vive `base.html`. |

### Código clave

Receta de arranque, desde la carpeta `Django`:

```bash
uv init --no-package --python 3.15 fase2
cd fase2
uv add django
rm main.py
uv run django-admin startproject config .
echo "db.sqlite3" >> .gitignore
uv run manage.py startapp inventario
uv run manage.py startapp pedidos
git branch --show-current          # si dice master: git branch -m main
```

`config/settings.py`:

```python
INSTALLED_APPS = [
    "inventario.apps.InventarioConfig",
    "pedidos.apps.PedidosConfig",
    "django.contrib.admin",
    # ... el resto de apps de Django
]

# dentro de TEMPLATES
"DIRS": [BASE_DIR / "templates"],

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
```

`config/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("inventario/", include("inventario.urls")),
    path("pedidos/", include("pedidos.urls")),
    path("admin/", admin.site.urls),
]
```

`inventario/urls.py`:

```python
from django.urls import path

from . import views

app_name = "inventario"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("materiales/", views.materiales, name="materiales"),
]
```

`templates/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block titulo %}Taller VHAJ{% endblock %}</title>
</head>
<body>
    <nav>
        <a href="{% url 'inventario:inicio' %}">Inventario</a>
        <a href="{% url 'inventario:materiales' %}">Materiales</a>
        <a href="{% url 'pedidos:inicio' %}">Pedidos</a>
    </nav>
    <main>
        {% block contenido %}{% endblock %}
    </main>
</body>
</html>
```

### Si vienes de Laravel

| Laravel | Django |
|---|---|
| `laravel new taller` | `uv init` + `uv add django` + `startproject config .` |
| `config/app.php` (`locale`, `timezone`) | `config/settings.py` (`LANGUAGE_CODE`, `TIME_ZONE`) |
| Todo el código va en `app/` | El proyecto se divide en apps |
| `routes/web.php` | `config/urls.py` + el `urls.py` de cada app |
| Nombres de ruta: `->name('inventario.inicio')` | `app_name` + `name`: `'inventario:inicio'` |
| `layouts/app.blade.php` con `@extends` y `@yield` | `templates/base.html` con `{% extends %}` y `{% block %}` |

### Errores típicos

| Qué hiciste mal | Qué te dice Django |
|---|---|
| `uv run manage.py` desde otra carpeta | `error: Failed to spawn: manage.py` |
| `startproject config` sin el punto | **Sin error**: queda una carpeta `config/config/` de más |
| Zona horaria mal escrita | `ValueError: Incorrect timezone setting: America/Bogata` |
| Idioma con guion bajo: `es_co` | `(translation.E001) You have provided an invalid value for the LANGUAGE_CODE setting: 'es_co'.` |
| Creaste una carpeta `templates` con el servidor encendido | `TemplateDoesNotExist` hasta que reinicias el servidor |
| `{% url 'inventario:inicio' %}` sin `app_name` en la app | `NoReverseMatch: 'inventario' is not a registered namespace` |

### Resumen

**Comandos**

```bash
uv init --no-package --python 3.15 nombre
uv add django
uv run django-admin startproject config .
uv run manage.py startapp nombre_app
uv run manage.py runserver
```

**Ideas clave**

- Cada proyecto nuevo arranca con la misma receta.
- `db.sqlite3` va en `.gitignore` desde el primer commit.
- Las apps se registran en `INSTALLED_APPS` antes de crear sus templates.
- Cada app tiene su `urls.py` con `app_name`, y el proyecto las conecta con `include()`.
- `base.html` vive en `templates/` (configurado en `DIRS`) y las páginas lo heredan con `{% extends %}`.
- Si creas una carpeta `templates` nueva, reinicia el servidor.

---

## Clase 1: Modelos y migraciones

### Conceptos

| Concepto | Qué es y para qué sirve |
|---|---|
| Modelo | Una clase de Python que describe una tabla de la base de datos. Hereda de `models.Model`. |
| Campo | Cada atributo de clase del modelo. Se convierte en una columna con su tipo de dato. |
| Migración | Un archivo que describe un cambio en la estructura de la base de datos. Es el historial de la base. |
| `makemigrations` | Crea las migraciones a partir de los cambios en los modelos. |
| `migrate` | Aplica las migraciones en la base de datos. |
| `id` automático | Django lo agrega solo. Desde Django 6.0 es de tipo `BigAutoField`. |

### Código clave

Campos más comunes:

| Campo | Para qué | Ejemplo |
|---|---|---|
| `CharField(max_length=...)` | Texto corto | Nombre, color |
| `TextField()` | Texto largo | Descripción |
| `IntegerField()` | Número entero; puede ser negativo | Ajustes |
| `PositiveIntegerField()` | Entero de 0 en adelante | Cantidad, gramos |
| `DecimalField(max_digits=..., decimal_places=...)` | Número decimal exacto | Precios |
| `BooleanField()` | Sí o no | Activo |
| `DateField()` | Fecha | Fecha de entrega |
| `DateTimeField(auto_now_add=True)` | Fecha y hora puestas solas al crear el registro | Fecha del pedido |

`default=...` es el valor que toma el campo si no le das uno. `max_length` ya no es obligatorio en SQLite ni en PostgreSQL, pero se pone siempre, porque Django lo usa para validar los formularios y el admin.

`inventario/models.py`:

```python
from django.db import models


class Material(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=30)
    cantidad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} {self.color}"
```

El ciclo de cada cambio en un modelo:

```bash
uv run manage.py makemigrations          # 1. crea el archivo de migración
uv run manage.py sqlmigrate inventario 0001   # (opcional) ver el SQL
uv run manage.py migrate                 # 2. aplica el cambio
uv run manage.py showmigrations          # [X] aplicada, [ ] pendiente
```

Tablas que crea el primer `migrate`:

| Tablas | Para qué |
|---|---|
| `auth_user`, `auth_group`, `auth_permission`… | Usuarios, grupos y permisos: el login y el admin |
| `django_session` | Las sesiones |
| `django_admin_log` | El historial de cambios hechos desde el admin |
| `django_content_type` | Un registro interno de los modelos |
| `django_migrations` | La "libreta" de migraciones aplicadas |
| `inventario_material`, `pedidos_pedido` | Las tuyas: `app_modelo`, en minúsculas |

### Si vienes de Laravel

| Laravel | Django |
|---|---|
| Escribes la migración a mano (`$table->string(...)`) | **Django la genera** a partir del modelo (`makemigrations`) |
| `php artisan migrate` | `uv run manage.py migrate` |
| `php artisan migrate:status` | `uv run manage.py showmigrations` |
| Tabla `migrations` | Tabla `django_migrations` |
| `$table->id()` | Automático |

### Errores típicos

| Qué hiciste mal | Qué te dice Django |
|---|---|
| Tipo mal escrito: `models.Charfield` | `AttributeError: module 'django.db.models' has no attribute 'Charfield'. Did you mean '.CharField' instead of '.Charfield'?` |
| Campo sin paréntesis: `color = models.CharField` | **Sin error**: `makemigrations` propone `- Remove field color from material` |
| Campo obligatorio nuevo, sin `default`, en un modelo con registros | `It is impossible to add a non-nullable field 'precio' to material without specifying a default...` |
| Cambiaste el modelo e hiciste `migrate` sin `makemigrations` | `Your models in app(s): 'inventario' have changes that are not yet reflected in a migration...` |
| Usaste el modelo sin haber hecho `migrate` | `OperationalError: no such table: inventario_material` |

### Resumen

**Comandos**

```bash
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py showmigrations
uv run manage.py sqlmigrate app 0001
```

**Ideas clave**

- Un modelo es una clase que hereda de `models.Model`, y cada atributo de clase es una columna.
- En Django no escribes migraciones: las genera `makemigrations`.
- El ciclo es: cambiar `models.py` → `makemigrations` → `migrate`.
- Lee la salida de `makemigrations` antes de `migrate`: un `-` (Remove) inesperado indica un error en el modelo.
- Las migraciones van a git; `db.sqlite3` no.
- La hora del encabezado de una migración está en UTC.

---

## Clase 2: Django Admin

### Conceptos

| Concepto | Qué es y para qué sirve |
|---|---|
| Django Admin | Un panel web que Django arma solo leyendo los modelos. Es para uso interno, no para los clientes. |
| Superusuario | Un usuario con todos los permisos. Solo entran al admin los usuarios marcados como personal (`is_staff`). |
| `admin.site.register` | Hace que un modelo aparezca en el admin. |
| `class Meta` | Una clase dentro del modelo con opciones del modelo, no campos. Por ejemplo, `verbose_name_plural`. |
| `ModelAdmin` | Una clase donde configuras cómo se ve y se comporta un modelo en el admin. |

### Código clave

```bash
uv run manage.py createsuperuser                 # crear el usuario del admin
uv run manage.py changepassword andfelipeme      # cambiar la contraseña
```

El plural en `inventario/models.py`. Cambiar `Meta` también genera una migración, aunque no toque la tabla (`sqlmigrate` muestra `(no-op)`):

```python
class Material(models.Model):
    # ... campos

    class Meta:
        verbose_name_plural = "materiales"

    def __str__(self):
        return f"{self.nombre} {self.color}"
```

`inventario/admin.py`:

```python
from django.contrib import admin

from .models import Material


class MaterialAdmin(admin.ModelAdmin):
    list_display = ["nombre", "color", "cantidad"]
    search_fields = ["nombre", "color"]
    list_filter = ["nombre"]


admin.site.site_header = "Taller VHAJ"
admin.site.register(Material, MaterialAdmin)
```

| Opción | Qué hace |
|---|---|
| `list_display` | Las columnas de la lista. Sin esta opción, solo hay una columna con el `__str__`. |
| `search_fields` | La caja de búsqueda. No distingue mayúsculas y busca texto que contenga lo escrito. |
| `list_filter` | Los filtros de la barra lateral. Para un texto, lista los valores; para una fecha, rangos (Hoy, Últimos 7 días…). |
| `readonly_fields` | Campos que se ven pero no se editan, como una fecha con `auto_now_add`. |

Otra forma de registrar, con un decorador (usa una de las dos, nunca ambas):

```python
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["nombre", "color", "cantidad"]
```

### Si vienes de Laravel

| Laravel (con Filament) | Django |
|---|---|
| `composer require filament/filament` | Ya viene incluido |
| `php artisan make:filament-user` | `createsuperuser` |
| Un *Resource* por modelo | Un `ModelAdmin` por modelo |
| `->columns([TextColumn::make('nombre')])` | `list_display = ["nombre"]` |
| `->searchable()` | `search_fields` |
| `->filters([...])` | `list_filter` |

### Errores típicos

| Qué hiciste mal | Qué te dice Django |
|---|---|
| No registraste el modelo | **Sin error**: el modelo no aparece en el admin |
| Falta el import del modelo | `NameError: name 'Material' is not defined` |
| Registraste el modelo dos veces | `AlreadyRegistered: The model Material is already registered with 'inventario.MaterialAdmin'.` |
| Campo inexistente en `list_display` | `(admin.E108) The value of 'list_display[3]' refers to 'precio', which is not a callable or attribute of 'MaterialAdmin', or an attribute, method, or field on 'inventario.Material'.` |
| Campo inexistente en `list_filter` | `(admin.E116) The value of 'list_filter[0]' refers to 'material', which does not refer to a Field.` |
| `("nombre")` sin coma en vez de una lista | `(admin.E107) The value of 'list_display' must be a list or tuple.` |
| Campo inexistente en `search_fields` | `FieldError: Cannot resolve keyword 'tipo' into field...`. `check` no lo detecta: el error sale al buscar |
| Usuario o contraseña incorrectos | `Por favor ingrese el nombre de usuario y la clave correctos para obtener cuenta de personal...` |
| El enlace "Ver el sitio" da 404 | El proyecto no tiene ruta en `/`. No es un error del admin |

### Resumen

**Comandos**

```bash
uv run manage.py createsuperuser
uv run manage.py changepassword usuario
```

**Ideas clave**

- El admin vive en `/admin/` y solo entran usuarios de personal (`is_staff`).
- `admin.site.register(Modelo, ModeloAdmin)` muestra el modelo con su configuración.
- `list_display`, `search_fields` y `list_filter` usan los nombres exactos de los campos.
- `class Meta` guarda opciones del modelo y también genera migración.
- Las contraseñas se guardan como hash, nunca en texto plano.
- El superusuario vive en `db.sqlite3`: en otro computador hay que crearlo otra vez.

---

## Clase 3: Consultas con el ORM

### Conceptos

| Concepto | Qué es y para qué sirve |
|---|---|
| ORM | Traduce Python a SQL: consultas la base de datos con métodos de Python. Es el equivalente de Eloquent. |
| `objects` (manager) | La puerta de entrada a la tabla: `Material.objects`. Se usa desde la clase, no desde un objeto. |
| QuerySet | El resultado de una consulta: una lista de objetos. Es perezoso: no consulta la base hasta que lo usas. |
| Lookup | La condición de un filtro, con doble guion bajo: `cantidad__lt=800`. |
| `shell` | Una consola de Python con el proyecto cargado y los modelos ya importados. |

### Código clave

```python
uv run manage.py shell                              # salir con exit()

Material.objects.all()                              # todos
Material.objects.count()                            # cuántos
Material.objects.filter(nombre="PLA")               # exacto (distingue mayúsculas)
Material.objects.filter(cantidad__lt=800)           # menor que
Material.objects.filter(cantidad__gte=1000)         # mayor o igual
Material.objects.filter(color__icontains="negro")   # contiene, sin importar mayúsculas
Material.objects.order_by("-cantidad", "nombre")    # - = descendente; el segundo desempata
Material.objects.filter(cantidad__gte=1000).count() # se pueden encadenar
Material.objects.get(id=2)                          # un solo objeto
Material.objects.filter(nombre="Nylon").first()     # el primero o None
```

| Lookup | Significa |
|---|---|
| sin lookup (`exact`) | Igual a |
| `__lt` / `__lte` | Menor que / menor o igual |
| `__gt` / `__gte` | Mayor que / mayor o igual |
| `__icontains` | Contiene el texto, sin importar mayúsculas |

La vista `inventario/views.py`:

```python
from django.shortcuts import render

from .models import Material


def materiales(request):
    lista = Material.objects.order_by("nombre", "color")
    contexto = {"titulo": "Materiales del taller", "materiales": lista}

    return render(request, "inventario/materiales.html", contexto)
```

El template no cambia al pasar de diccionarios a objetos: `{{ material.nombre }}` lee igual una clave que un atributo.

### Si vienes de Laravel

| Laravel | Django |
|---|---|
| `php artisan tinker` | `uv run manage.py shell` |
| `Material::all()` | `Material.objects.all()` |
| `Material::count()` | `Material.objects.count()` |
| `Material::where('nombre', 'PLA')->get()` | `Material.objects.filter(nombre="PLA")` |
| `Material::where('cantidad', '<', 800)->get()` | `Material.objects.filter(cantidad__lt=800)` |
| `Material::orderBy('cantidad', 'desc')->get()` | `Material.objects.order_by("-cantidad")` |
| `Material::findOrFail(2)` | `Material.objects.get(id=2)` |
| Colección (Collection) | QuerySet |

En Eloquent la consulta se ejecuta con `->get()`. En Django se ejecuta sola cuando usas el QuerySet.

### Errores típicos

| Qué hiciste mal | Qué te dice Django |
|---|---|
| `Material.all()` sin `objects` | `AttributeError: type object 'Material' has no attribute 'all'. Did you mean '.objects.all' instead of '.all'?` |
| `objects` desde un objeto: `m.objects` | `AttributeError: Manager isn't accessible via Material instances` |
| Campo mal escrito en `filter` u `order_by` | `FieldError: Cannot resolve keyword 'nombr' into field. Choices are: cantidad, color, id, nombre` |
| Lookup que no existe: `cantidad__menor=5` | `FieldError: Unsupported lookup 'menor' for PositiveIntegerField or join on the field not permitted.` |
| `get()` sin resultados | `Material.DoesNotExist: Material matching query does not exist.` |
| `get()` con varios resultados | `Material.MultipleObjectsReturned: get() returned more than one Material -- it returned 2!` |
| `filter(nombre="pla")` con el dato "PLA" | **Sin error**: `<QuerySet []>` |
| La vista usa el modelo sin importarlo | Error 500: `name 'Material' is not defined` |
| `get()` en la vista y `{% for %}` en el template | Error 500: `'Material' object is not iterable` |

### Resumen

**Comandos**

```python
uv run manage.py shell
Material.objects.all()
Material.objects.count()
Material.objects.filter(cantidad__lt=800)
Material.objects.order_by("-cantidad")
Material.objects.get(id=2)
Material.objects.filter(nombre="X").first()
```

**Ideas clave**

- Las consultas se hacen desde la clase, con `objects`.
- `all`, `filter` y `order_by` devuelven un QuerySet; `get` y `first`, un objeto; `count`, un número.
- Los lookups llevan doble guion bajo: `__lt`, `__gte`, `__icontains`.
- Sin `order_by` el orden no está garantizado. En las vistas, ordena siempre y con desempate si hace falta.
- `get` da error si no encuentra nada o encuentra varios; `first` devuelve `None`.
- En el template, `{{ objeto.campo }}` funciona igual que con un diccionario.

---

## Clase 4: Relaciones entre modelos (`ForeignKey`)

### Conceptos

| Concepto | Qué es y para qué sirve |
|---|---|
| Relación muchos a uno | Muchos pedidos pueden usar el mismo material, pero cada pedido usa un solo material. |
| `ForeignKey` | El campo que crea la relación. Va en el modelo del lado "muchos": `Pedido`. |
| `material_id` | La columna real en la base de datos. Guarda el `id` del material. |
| `on_delete` | Qué pasa con los pedidos si se borra su material. Es obligatorio. |
| `pedido_set` | El acceso inverso: desde un material llegas a sus pedidos. |

### Código clave

`pedidos/models.py`:

```python
from django.db import models


class Pedido(models.Model):
    cliente = models.CharField(max_length=100)
    pieza = models.CharField(max_length=100)
    material = models.ForeignKey("inventario.Material", on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente} - {self.pieza}"
```

- `"inventario.Material"` es una referencia `"app.Modelo"` entre comillas, así que no hace falta importar el modelo.

| `on_delete` | Qué pasa al borrar el material | Cuándo usarlo |
|---|---|---|
| `CASCADE` | Borra también sus pedidos | Datos que no tienen sentido sin el otro |
| `PROTECT` | No deja borrarlo (`ProtectedError`) | No perder el historial de pedidos |
| `SET_NULL` | Deja el campo en nulo; necesita `null=True` | Relaciones opcionales |

Si ya hay pedidos, `makemigrations` pide un valor inicial: opción `1` y luego el **`id`** de un material que exista (por ejemplo `1`), no su nombre.

```python
pedido.material                                 # adelante: el material del pedido
pedido.material.nombre
pedido.material_id                              # solo el id
material.pedido_set.all()                       # atrás: los pedidos del material
material.pedido_set.count()
Pedido.objects.filter(material__nombre="PLA")   # filtrar cruzando la relación
```

En el admin, la `ForeignKey` aparece como una lista desplegable con el `__str__` de cada material. En `ModelAdmin`, `"material"` funciona como un campo más, y `"material__nombre"` cruza la relación en `search_fields`.

### Si vienes de Laravel

| Laravel | Django |
|---|---|
| `$table->foreignId('material_id')->constrained()` | `models.ForeignKey("inventario.Material", on_delete=...)` |
| `->cascadeOnDelete()` / `->restrictOnDelete()` / `->nullOnDelete()` | `CASCADE` / `PROTECT` / `SET_NULL` |
| `belongsTo(Material::class)` | No hace falta: la `ForeignKey` ya da `pedido.material` |
| `hasMany(Pedido::class)` | No hace falta: Django crea `material.pedido_set` |
| `$pedido->material->nombre` | `pedido.material.nombre` |
| `$material->pedidos()->count()` | `material.pedido_set.count()` |
| `Pedido::whereHas('material', fn ($q) => $q->where('nombre', 'PLA'))->get()` | `Pedido.objects.filter(material__nombre="PLA")` |

### Errores típicos

| Qué hiciste mal | Qué te dice Django |
|---|---|
| Olvidaste `on_delete` | `TypeError: ForeignKey.__init__() missing 1 required positional argument: 'on_delete'` |
| Modelo mal escrito: `"inventario.Materiales"` | `(fields.E300) Field defines a relation with model 'inventario.Materiales', which is either not installed, or is abstract.` |
| Sin la app: `"Material"` | `(fields.E307) ... lazy reference to 'pedidos.material', but app 'pedidos' doesn't provide model 'material'.` |
| Sin comillas y sin import: `ForeignKey(Material, ...)` | `NameError: name 'Material' is not defined` |
| `SET_NULL` sin `null=True` | `(fields.E320) Field specifies on_delete=SET_NULL, but cannot be null.` |
| En el valor inicial escribiste `PLA` en vez del `id` | `NameError: name 'PLA' is not defined` (deja intentarlo otra vez) |
| Diste un `id` que no existe (`99`) | `migrate` falla con `IntegrityError: ... contains a value '99' that does not have a corresponding value in inventario_material.id.` Borra la `0002` (no se aplicó) y repite `makemigrations` |
| `material.pedidos` | `AttributeError: 'Material' object has no attribute 'pedidos'. Did you mean '.pedido_set' instead of '.pedidos'?` |
| Borrar un material que tiene pedidos | En el admin: `No se puede eliminar material` y la lista de pedidos protegidos |

### Resumen

**Comandos**

```python
material = models.ForeignKey("inventario.Material", on_delete=models.PROTECT)
pedido.material
material.pedido_set.all()
material.pedido_set.count()
Pedido.objects.filter(material__nombre="PLA")
```

**Ideas clave**

- La `ForeignKey` va en el lado "muchos" y crea la columna `campo_id`.
- `on_delete` es obligatorio. `PROTECT` impide borrar algo que está en uso.
- Si ya hay registros, `makemigrations` pide un valor inicial: un `id` que exista.
- Hacia adelante: `pedido.material`. Hacia atrás: `material.pedido_set`.
- Con `__` cruzas la relación: `material__nombre`.
- Un método en el modelo (como `cantidad_pedidos()`) no cambia la tabla: no necesita migración.

---

## Prácticas realizadas

| Práctica | Qué hice | Resultado |
|---|---|---|
| 0. Repaso del arranque | Proyecto `fase2` desde cero: dos apps, URLs con `app_name`, `base.html` con menú, vistas con templates | ✅ |
| 1. Modelo `Pedido` | Modelo con `cliente`, `pieza`, `cantidad` y `fecha` automática; migración creada y aplicada | ✅ |
| 2. Admin de `Pedido` | Superusuario; `PedidoAdmin` con columnas, búsqueda, filtro por fecha y `fecha` de solo lectura; plural "materiales"; datos cargados. Reto: encabezado "Taller VHAJ" | ✅ |
| 3. Pedidos desde la base de datos | Vista con los pedidos del más reciente al más antiguo, fecha en el template, consultas en el `shell` | ✅ |
| 4. Material de cada pedido | `ForeignKey` con `PROTECT`; columna, filtro y búsqueda por material en el admin; material en `/pedidos/`. Reto: método `cantidad_pedidos()` | ✅ |

**Consultas del `shell` de las prácticas 3 y 4** (con los datos del 26 de noviembre de 2026):

```python
>>> Pedido.objects.count()
4
>>> Pedido.objects.filter(cantidad__gte=3)
<QuerySet [<Pedido: Juan - 0002.stl>, <Pedido: Andres - 0004.stl>]>
>>> Pedido.objects.filter(pieza__icontains="0001")
<QuerySet [<Pedido: Pepito - 0001.stl>]>
>>> Pedido.objects.order_by("-fecha")
<QuerySet [<Pedido: Andres - 0004.stl>, <Pedido: Lucas - 0003.stl>, <Pedido: Juan - 0002.stl>, <Pedido: Pepito - 0001.stl>]>
>>> Pedido.objects.get(cliente="Lucas").material
<Material: TPU Amarillo>
>>> Material.objects.get(id=4).pedido_set.count()
1
>>> Pedido.objects.filter(material__nombre="PLA")
<QuerySet [<Pedido: Pepito - 0001.stl>, <Pedido: Andres - 0004.stl>]>
>>> Pedido.objects.filter(material__nombre="PLA").count()
2
```

## Lecciones de las revisiones

- Las migraciones van en el commit junto con el cambio del modelo; `db.sqlite3` nunca.
- La hora del encabezado de una migración está en UTC (00:33 UTC son las 19:33 en Bogotá). En la base de datos las fechas también se guardan en UTC, y el admin y los templates las muestran en hora de Bogotá.
- Si ordenas por un campo que se repite (dos PLA), agrega un segundo campo para desempatar: `order_by("nombre", "color")`.
- La etiqueta debe decir lo mismo que el dato: `Pieza:` para el campo `pieza`, y sin mayúsculas en medio de la frase.
- `list_filter = ["material"]` filtra por material (los 4); `["material__nombre"]` filtra por el nombre del material y mezcla los colores.
- Orden dentro del modelo: campos, `class Meta`, `__str__` y después los métodos propios.
- Mismo estilo en todo el template: `{{ pedido.material }}`, con espacios, igual que los demás.
- Borra los comentarios de ejemplo que deja Django, como `# Create your views here.`
- Ruff marca `RUF012` en las listas de los `admin.py`. No es un error de Django; se resuelve al configurar Ruff.
