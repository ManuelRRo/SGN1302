from django.contrib import admin
from .models import (
    Alumno,Categoria,Docente,Evaluacion,
    Evaluacionalumno,Grado,Gradoseccion,
    Gradoseccionmateria,Materia,Seccion,Trimestre,)

admin.site.register(Alumno)
admin.site.register(Categoria)
admin.site.register(Docente)
admin.site.register(Evaluacion)
admin.site.register(Evaluacionalumno)
admin.site.register(Grado)
#admin.site.register(Gradoseccion)
admin.site.register(Gradoseccionmateria)
admin.site.register(Materia)
admin.site.register(Seccion)
admin.site.register(Trimestre)

@admin.register(Gradoseccion)
class GradoSeccionAdmin(admin.ModelAdmin):
    list_display = ['id_grado','id_seccion','nivel']