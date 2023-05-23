from django.urls import path
from . import  views
app_name = "sgn_app"
urlpatterns = [
    path(
        '',
        views.home,
        name="home"
    ),
    path(
        'estudiante/crear-eva-est',
        views.CrearEvaluacionAlumno,
        name="crear_eva_est"
    ),
    path(
        'estudiante/list-evas-not/',
        views.ListarEvaluacionesAlumnos.as_view(),
        name="list_evas_not"
    ),
    path(
        'estudiante/edit-evas-not/<int:pk>/',
        views.ActualizarEvaluacionesAlumno.as_view(),
        name="edit_evas_not"
    ),
]