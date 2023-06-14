from django.forms import ModelForm
from django import forms
from .models import Evaluacion, Evaluacionalumno, Docente,Alumno,Trimestre,Categoria,Gradoseccionmateria
from django.core.exceptions import ValidationError


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_categoria', 'id_gradoseccionmateria',
                  'nombre_evaluacion', 'porcentaje', 'id_trimestre']
        widgets = {
            'id_categoria': forms.Select(attrs={'class':'form-control form-control-lg'}),
            'id_gradoseccionmateria': forms.Select(attrs={'class':'form-control form-control-lg'}),
            'nombre_evaluacion': forms.TextInput(attrs={'class':'form-control form-control-lg','placeholder':'Nombre Evaluación'}),
            'porcentaje': forms.NumberInput(attrs={'class':'form-control form-control-lg','placeholder':'Porcentaje'}),
            'id_trimestre': forms.Select(attrs={'class':'form-control form-control-lg'}),
        }
        labels = {
            'id_categoria': 'Categoria',
			'nombre_evaluacion': 'Nombre Evaluacion',
            'id_gradoseccionmateria': ' Grado y Materia',
            'id_trimestre':'Trimestre'
			
        }
    

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


class DocenteForm(forms.ModelForm):
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

#HU-33 Crear Trimestre
class TrimestreForm(forms.ModelForm):
    class Meta:
        model = Trimestre
        fields = [
            'trimestre',
            'anio',]
        widgets={
            'trimestre': forms.TextInput(
               attrs= { 
                'placeholder': 'Nombre Trimestre',
                'class':'form-control form-control-lg',
                'id':'updateNombreTrim'
                }
            ),
            'anio': forms.NumberInput(
               attrs= {
                'placeholder': 'Año Trimestre',
                'class':'form-control form-control-lg',
                'id':'updaterYearTrim'
                }
            )
        }


class TrimestreActualizarForm(forms.ModelForm):
    """Form definido para actualizar Trimestre."""

    class Meta:
        model = Trimestre
        fields = ('trimestre',
                  'anio')
        widgets={
            'trimestre': forms.TextInput(
               attrs= { 
                'placeholder': 'Nombre Trimestre',
                'class':'form-control form-control-lg',
                'id':'updateNombreTrim'

                }
            ),
            'anio': forms.NumberInput(
               attrs= {
                'placeholder': 'año Trimestre',
                'class':'form-control form-control-lg',
                'id':'updaterYearTrim'
                }
            )
        }

class EvaluacionEditarForm(forms.ModelForm):
    """Form definido para actualizar Evaluacion."""
    class Meta:
        model = Evaluacion
        fields = ('id_categoria',
                  'id_gradoseccionmateria',
                  'id_trimestre',
                  'nombre_evaluacion',
                  'porcentaje')
        widgets={
            'id_categoria': forms.Select(
               attrs= {
                'class':'form-select form-select-lg mb-3 mt-4',
                
                }
            ), 
            'id_gradoseccionmateria': forms.Select(
               attrs= {
                'class':'form-select form-select-lg mb-3 mt-4',
                
                }
            ),
            'nombre_evaluacion': forms.TextInput(
               attrs= {
                'placeholder': 'nombre de Evaluación',
                'class':'form-control form-control-lg mt-4',
                'id':'nameUpdateEva' 
                }
            ),
            'porcentaje': forms.NumberInput(
               attrs= {
                'placeholder': 'porcentaje de Evaluación',
                'class':'form-control form-control-lg mt-4',
                'id':'percentageUpdateEva'
                }
            )

        }

#HU-21
class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'id_gradoseccion',
            'nie',
            'apellidos_alumno',
            'nombres_alumno'
        ]



