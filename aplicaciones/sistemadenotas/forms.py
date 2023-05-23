from django.forms import ModelForm
from django import forms
from .models import Evaluacion
from django.core.exceptions import ValidationError

class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_categoria','id_gradoseccionmateria','nombre_evaluacion','porcentaje']

    def clean_nombre_evaluacion(self):
        nom_evaluacion = self.cleaned_data['nombre_evaluacion']
        lista = Evaluacion.objects.filter(nombre_evaluacion=nom_evaluacion).exclude(id_evaluacion=self.instance.id_evaluacion)
        if lista:
            self.add_error('nombre_evaluacion','Esa evaluacion ya existe')
        return nom_evaluacion

                 

    
            #      
            # lista = Evaluacion.objects.filter(correo=nom_evaluacion).exclude(id=self.instance.id)
            # if lista:
            #     self.add_error('nombre_evaluacion','Esa evaluacion ya existe')

            # return nom_evaluacion
           