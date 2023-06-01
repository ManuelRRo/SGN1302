from django.urls import path
from django.contrib.auth.decorators import login_required
from . import  views
app_name = "sgn_app"
urlpatterns = [
    path(
        '',
        views.home,
        name="home"
    ),
    path(
        'evaluacion/listar-evas-grado/<idgrado>/',
        views.ListarEvaluacionesGrados.as_view(),
        name="listar_evas_grado"
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
    path(
        'estudiante/crear-eva-est',
        views.CrearEvaluacionAlumno,
        name="crear_eva_est"
    ),
    
    # Gestión de Docentes
    path(
        'listado_docentes/',
        login_required(views.ListarDocentes.as_view()),
        name='listado_docentes'
    ),
    path('crear_docente/',
        login_required(views.CrearDocentes.as_view()),
        name='crear_docente'
    ),
]