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
        'estudiante/list-evas-not/<idEvaluacion>/',
        views.ListarEvaluacionesAlumnos.as_view(),
        name="list_evas_not"
    ),
    path(
        'estudiante/crear-eva-est',
        views.CrearEvaluacionAlumno,
        name="crear_eva_est"
    ),
    #HU-21
    path(
        'estudiante/crear-estudiante',
        views.CrearAlumno.as_view(),
        name="crear_alumno"
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
    path(
        'actualizarTrimestre/<pk>/',
        views.ActualizarTrimestre.as_view(),
        name='modificar_trimestre'
    ),
    path(
        'correcto/',
        views.Correcto.as_view(),
        name='correcto'
    ),
    path(
        'editarEvaluacion/<pk>/',
        views.EvaluacionEditar.as_view(),
        name='actualizar_evaluacion'

    ),
    # Vista de habilitar o deshabilitar alumnos
    


]