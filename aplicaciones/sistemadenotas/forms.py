from django.forms import ModelForm
from django import forms
from .models import Evaluacion, Evaluacionalumno, Docente, Trimestre
from django.core.exceptions import ValidationError



class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_categoria', 'id_gradoseccionmateria',
                  'nombre_evaluacion', 'porcentaje', 'id_trimestre']

    def clean_nombre_evaluacion(self):
        nom_evaluacion = self.cleaned_data['nombre_evaluacion']
        lista = Evaluacion.objects.filter(nombre_evaluacion__icontains=nom_evaluacion).exclude(
            id_evaluacion=self.instance.id_evaluacion)
        if lista:
            self.add_error('nombre_evaluacion', 'Esa evaluacion ya existe')
        return nom_evaluacion


class EvaluacionAlumnoForm(ModelForm):
    class Meta:
        model = Evaluacionalumno
        fields = ['id_evaluacionalumno', 'id_evaluacion', 'id_alumno', 'nota']

# Formulario DOCENTE


class DocenteForm(ModelForm):
    class Meta:
        model = Docente
        fields = [
            'numidentificacion',
            'dui',
            'nombre_docente',
            'apellido_docente']
    
    def clean_numidentificacion(self):
        username = self.cleaned_data['numidentificacion']
        lista = Docente.objects.filter(numidentificacion__icontains=username).exclude(
            id_docente=self.instance.id_docente)
        if lista:
            self.add_error('numidentificacion', 'Esa username ya existe')
        return username

class TrimestreActualizarForm(forms.ModelForm):
    """Form definition for TrimestreActualizar."""

    class Meta:
        model = Trimestre
        fields = ('trimestre',
                  'anio')
        widgets={
            'trimestre': forms.TextInput(
               attrs= {
                'placeholder': 'Nombre Trimestre',
                'class':'entradaTxt'

                }
            ),
            'anio': forms.NumberInput(
               attrs= {
                'placeholder': 'año Trimestre',
                'class':'entradaTxt',
                'id':'actualizar'
                }
            )
        }



