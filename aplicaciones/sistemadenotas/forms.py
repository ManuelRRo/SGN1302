from django.forms import ModelForm
from django import forms
from .models import Evaluacion, Evaluacionalumno, Docente, Alumno, Trimestre
from django.core.exceptions import ValidationError


class EvaluacionForm(ModelForm):
    class Meta:
        model = Evaluacion
        fields = ['id_categoria', 'id_gradoseccionmateria',
                  'nombre_evaluacion', 'porcentaje', 'id_trimestre']
        widgets = {
            'id_categoria': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'id_gradoseccionmateria': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'nombre_evaluacion': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Nombre Evaluación'}),
            'porcentaje': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Porcentaje'}),
            'id_trimestre': forms.Select(attrs={'class': 'form-control form-control-lg'}),
        }
        labels = {
            'id_categoria': 'Categoria',
            'nombre_evaluacion': 'Nombre Evaluacion',
            'id_gradoseccionmateria': ' Grado y Materia',
            'id_trimestre': 'Trimestre'
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

# HU-33 Crear Trimestre
class MySelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=(), *args, **kwargs):
        default_attrs = {
            'class': 'form-control form-control-lg',  # Agrega tus clases de estilo personalizadas aquí
            'id': 'updateNombreTrim',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs, choices=choices, *args, **kwargs)

class TrimestreForm(forms.ModelForm):
    trimestre = forms.ChoiceField(
        choices=[('Primer Trimestre', 'Primer Trimestre'), ('Segundo Trimestre', 'Segundo Trimestre'), ('Tercer Trimestre', 'Tercer Trimestre')],
        widget=MySelectWidget,  # nuestro widget personalizado
    )

    class Meta:
        model = Trimestre
        fields = [
            'trimestre',
            'anio',
        ]
        widgets = {
            'anio': forms.NumberInput(
                attrs={
                    'placeholder': 'Año Trimestre',
                    'class': 'form-control form-control-lg',
                    'id': 'updaterYearTrim',
                }
            ),
        }


class TrimestreActualizarForm(forms.ModelForm):
    """Form definido para actualizar Trimestre."""

    class Meta:
        model = Trimestre
        fields = ('trimestre',
                  'anio')
        widgets = {
            'trimestre': forms.TextInput(
                attrs={
                    'placeholder': 'Nombre Trimestre',
                    'class': 'form-control form-control-lg',
                    'id': 'updateNombreTrim'

                }
            ),
            'anio': forms.NumberInput(
                attrs={
                    'placeholder': 'año Trimestre',
                    'class': 'form-control form-control-lg',
                    'id': 'updaterYearTrim'
                }
            )
        }


class EvaluacionEditarForm(forms.ModelForm):
    """Form definido para actualizar Evaluacion."""
    class Meta:
        model = Evaluacion
        exclude = ('id_trimestre',)
        fields = ('id_categoria',
                  'id_gradoseccionmateria',
                  'id_trimestre',
                  'nombre_evaluacion',
                  'porcentaje')
        widgets = {
            'id_categoria': forms.Select(
                attrs={
                    'class': 'form-select form-select-lg mb-3 mt-4',

                }
            ),
            'id_gradoseccionmateria': forms.Select(
                attrs={
                    'class': 'form-select form-select-lg mb-3 mt-4',

                }
            ),
            'nombre_evaluacion': forms.TextInput(
                attrs={
                    'placeholder': 'nombre de Evaluación',
                    'class': 'form-control form-control-lg mt-4',
                    'id': 'nameUpdateEva'
                }
            ),
            'porcentaje': forms.NumberInput(
                attrs={
                    'placeholder': 'porcentaje de Evaluación',
                    'class': 'form-control form-control-lg mt-4',
                    'id': 'id_porcentaje'
                }
            )

        }

# HU-21 y HU-24


class AlumnoForm(ModelForm):
    class Meta:
        model = Alumno
        fields = [
            'id_gradoseccion',
            'nie',
            'apellidos_alumno',
            'nombres_alumno',
            'estado',
            'sexo'
        ]
        ACTIVO = "1"
        INACTIVO = "0"
        ESTADO_CHOICES = [
            (ACTIVO, "ACTIVO"),
            (INACTIVO, "INACTIVO"),
        ]
        widgets = {
            'id_gradoseccion': forms.Select(attrs={'class': 'form-control form-control-lg'}),
            'nie': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'NIE'}),
            'apellidos_alumno': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Apellidos'}),
            'nombres_alumno': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Nombres'}),
            'estado': forms.Select(attrs={'class': 'form-control form-control-lg',
                                           'placeholder': 'Estado'}, choices=ESTADO_CHOICES),
            'sexo': forms.Select(attrs={'class': 'form-control form-control-lg',}),
        }
        labels = {
            'id_gradoseccion': 'Grado y seccion',
            'nie': 'NIE',
            'apellidos_alumno': 'Apellidos Alumno',
            'nombres_alumno': 'Nombre Alumno',
            'estado': 'Estado del alumno'
        }



