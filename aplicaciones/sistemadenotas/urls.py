from django.urls import path
from django.contrib.auth.decorators import login_required
from . import  views
from .views import deshabilitar_usuario
from .views import habilitar_usuario
from .views import deshabilitar_evaluacion
from .views import habilitar_evaluacion

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
    # HU-14: Reporte de Alumnos Aprobados/Reprobados
    path('graficoAR/<aprobados>/<reprobados>/<gradoseccionmateria>',views.graficoAR, name='graficoAR'),
    #HU-15:Reporte de Alumnos Masculinos/Femeninos
    path('graficosEstadisticos/',views.graficos, name='graficos'),
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
       #HU-22: Editar Alumnos
    path(
        'Actualizar_Alumnos/<int:pk>/<id_gradoseccion>/',
        login_required(views.ActualizarAlumno.as_view()),
        name='ActualizarAlumno'
    ),
    #HU-24: Listar Alumnos
    path(
        'Listar_Alumnos/<id_gradoseccion>/',
        login_required(views.ListarAlumno.as_view()),
        name='ListarAlumno'
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
    path(
        'editar_docente_password/<str:id>', 
        views.EditarDocenteContra, 
        name='editar_docente_password'
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
    #HU-33: Crear Trimestre
    path(
        'crear_trimestre',
        views.CrearTrimestre, 
        name='crear_trimestre'
    ),
    # HU-34: Listar Trimestres
    path(
        'listar_trimestres/',
        login_required(views.ListarTrimestres.as_view()),
        name='listar_trimestres'
    ),
    # HU-35: Actualizar Trimestre
    path(
        'actualizarTrimestre/<pk>/',
        views.ActualizarTrimestre.as_view(),
        name='modificar_trimestre'
    ),
    path(
        'eliminar_trimestre/<int:id>', 
        views.EliminarTrimestre,
        name = 'eliminar_trimestre'
    ),
    #----------------------------------------------

    # ---------------------------------------------
    # HU-38: Listar Evaluaciones
    path(
        'evaluacion/listar_evaluaciones',
        views.ListarEvaluaciones.as_view(),
        name="listar_evaluaciones"
    ),
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
        'editarEvaluacionDocente/<idEvaluacion>/',
        views.evaluacion_editar_docente,
        name='actualizar_evaluacion_docente'
    ),
    path(
        'verPromedios/<int:idgrado>/<int:idtrimestre>/',
        views.ver_Promedios,
        name="ver_Promedios"
    ),
    path(
        'cambiar_Rol/',
        views.cambiarRolListView.as_view(),
        name = 'Cambio de rol'
    ),
    path('cambiar_Rol/<str:nombreUsuario>/', 
        views.Cambiar_Rol, 
        name='cambio_rol'
    ),
    path(
        'excelAlumnos/<int:id>/', 
        views.excelAlumnos, 
        name='excelAlumnos'
    ),
    path(
        'confirmar-importacion/<int:id>/', 
        views.confirmar_importacion,
        name='confirmar_importacion'
        ),

    # HU-39: Habilitar/Deshabilitar Evaluación
    path(
        'deshabilitar_evaluacion/<int:idgsm>/<int:idtri>/<int:id>/', 
        deshabilitar_evaluacion, 
        name='deshabilitar_evaluacion'
    ),
    path(
        'habilitar_evaluacion/<int:idgsm>/<int:idtri>/<int:id>/', 
        habilitar_evaluacion, 
        name='habilitar_evaluacion'
    ),
]