from django.forms import ModelForm
from django import forms
from .models import Evaluacion,Evaluacionalumno
from django.core.exceptions import ValidationError

class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_categoria','id_gradoseccionmateria','nombre_evaluacion','porcentaje','id_trimestre']

    def clean_nombre_evaluacion(self):
        nom_evaluacion = self.cleaned_data['nombre_evaluacion']
        lista = Evaluacion.objects.filter(nombre_evaluacion__icontains=nom_evaluacion).exclude(id_evaluacion=self.instance.id_evaluacion)
        if lista:
            self.add_error('nombre_evaluacion','Esa evaluacion ya existe')
        return nom_evaluacion

class EvaluacionAlumnoForm(ModelForm):
    class Meta:
        model = Evaluacionalumno
        fields = ['id_evaluacionalumno','id_evaluacion','id_alumno','nota']

                 

    
           