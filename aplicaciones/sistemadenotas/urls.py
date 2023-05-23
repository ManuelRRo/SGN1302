from django.urls import path
from . import  views
app_name = "sgn_app"
urlpatterns = [
    path('',views.home,name="home"),
    path(
        'estudiante/crear-eva-est',
        views.CrearEvaluacionAlumno,
        name="crear_eva_est"
    ),
]