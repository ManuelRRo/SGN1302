from django.urls import path
from django.contrib.auth.decorators import login_required
from . import  views
from .views import deshabilitar_usuario
from .views import habilitar_usuario

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
    path(
        'habilitarDeshabilitarAlumno/<id>/',
        login_required(views.HabDeshabiAlumno.as_view()),
        name='Habilitar-DeshabilitarAlumno'
    ),
    path(
        'habilitarDeshabilitarAlumno/<id>/deshabilitarAlumno/<idAlumno>/',
        views.deshabilitar
    ),
     path(
        'habilitarDeshabilitarAlumno/<id>/habilitarAlumno/<idAlumno>/',
        views.habilitar
    )
    # Vista de habilitar o deshabilitar alumnos
    



    path('editar/<str:id>', views.EditarDocente, name='editar_docente'),

    path('deshabilitar-usuario/<str:id>/', deshabilitar_usuario, name='deshabilitar_usuario'),

    path('habilitar-usuario/<str:id>/', habilitar_usuario, name='habilitar_usuario'),

]