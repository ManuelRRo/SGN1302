from django.urls import path
from django.contrib.auth.decorators import login_required
from . import  views
from .views import deshabilitar_usuario
from .views import habilitar_usuario

app_name = "sgn_app"
urlpatterns = [
    # Inicio de la aplicación
    # HU-01: Listar Grados Asignados
    path(
        '',
        views.home,
        name="home"
    ),
    # HU-02: Listar Evaluaciones del Grado
    path(
        'evaluacion/listar-evas-grado/<idgrado>/',
        views.ListarEvaluacionesGrados.as_view(),
        name="listar_evas_grado"
    ),
    # HU-04: Ingresar Notas de Alumnos por Evaluación
    # HU-05: Actualizar Notas de Alumnos por Evaluación
    path(
        'estudiante/list-evas-not/<idEvaluacion>/',
        views.ListarEvaluacionesAlumnos.as_view(),
        name="list_evas_not"
    ),
    # HU-08: Generar archivo de excel de notas trimestrales 
     path(
        'generarNotaExcel/',
        views.ReporteDeNotasExcel.as_view(),
        name="reporteExcel"
    ),
    # Gestión Alumnos -----------------------------
    # HU-21: Insertar Alumnos
    path(
        'estudiante/crear-estudiante',
        views.CrearAlumno.as_view(),
        name="crear_alumno"
    ),
    # HU-23: Habilitar/Deshabilitar Alumnos 
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
    ),
    # -------------------------------------------

    # Gestión de Docentes -----------------------
    # HU-28: Asignación de Grado/Seccion con Materia
    path('asignar_clases',
        login_required(views.AsignacionClases.as_view()),
        name='asignar_clases'
    ),
    path('eliminar_asignar_clases/<id>/',
        views.EliminarAsigacionClases,
        name='eliminar_asignar_clases'
    ),
    # HU-29: Agregar Docentes
    path('crear_docente/',
        login_required(views.CrearDocentes.as_view()),
        name='crear_docente'
    ),
    # HU-30: Editar Docentes
    path(
        'editar_docente/<str:id>', 
        views.EditarDocente, 
        name='editar_docente'
    ),
    # HU-31: Habilitar/Deshabilitar Docentes
    path(
        'deshabilitar-usuario/<str:id>/', 
        deshabilitar_usuario, 
        name='deshabilitar_usuario'
    ),
    path(
        'habilitar-usuario/<str:id>/', 
        habilitar_usuario, 
        name='habilitar_usuario'
    ),
    # HU-32: Listar Docentes
    path(
        'listado_docentes/',
        login_required(views.ListarDocentes.as_view()),
        name='listado_docentes'
    ),
    # -------------------------------------------

    # Gestión Trimestres -------------------------
    # HU-35: Actualizar Trimestre
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
    #----------------------------------------------

    # ---------------------------------------------
    # HU-38: Agregar Evaluación
    path(
        'estudiante/crear-eva-est',
        views.CrearEvaluacionAlumno,
        name="crear_eva_est"
    ),
    # HU-40: Editar Evaluación
    path(
        'editarEvaluacion/<pk>/',
        views.EvaluacionEditar.as_view(),
        name='actualizar_evaluacion'
    ),
    path(
        'verPromedios/<idgrado>/',
        views.ver_Evaluaciones,
        name="ver_Promedios"

    ),
]