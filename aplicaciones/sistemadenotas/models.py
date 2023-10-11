from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError


class Alumno(models.Model):
    class Sexo(models.TextChoices):
        MASCULINO = 'M','Masculino'
        FEMENINO = 'F', 'Femenino'

    id_alumno = models.AutoField(db_column='ID_ALUMNO', primary_key=True)  # Field name made lowercase.
    id_gradoseccion = models.ForeignKey('Gradoseccion', models.DO_NOTHING, db_column='ID_GRADOSECCION', blank=True, null=True)  # Field name made lowercase.
    nie = models.CharField(db_column='NIE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    apellidos_alumno = models.CharField(db_column='APELLIDOS_ALUMNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nombres_alumno = models.CharField(db_column='NOMBRES_ALUMNO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='HABILITADO',max_length=1,null=True)
    sexo = models.CharField(db_column="SEXO", max_length=1,null=False,choices=Sexo.choices,default=Sexo.FEMENINO)
    class Meta:
        managed = False
        db_table = 'alumno'
    def __str__(self) -> str:
        return self.nombres_alumno + ' ' + self.apellidos_alumno


class Categoria(models.Model):
    id_categoria = models.AutoField(db_column='ID_CATEGORIA', primary_key=True)  # Field name made lowercase.
    nombre_categoria = models.CharField(db_column='NOMBRE_CATEGORIA', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'categoria'
    def __str__(self) -> str:
        return self.nombre_categoria


class Docente(models.Model):
    id_docente = models.AutoField(db_column='ID_DOCENTE', primary_key=True)  # Field name made lowercase.
    numidentificacion = models.CharField(db_column='NUMIDENTIFICACION', max_length=8, blank=True, null=True)  # Field name made lowercase.
    dui = models.CharField(db_column='DUI', max_length=8, blank=True, null=True, unique=True)  # Field name made lowercase.
    nombre_docente = models.CharField(db_column='NOMBRE_DOCENTE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellido_docente = models.CharField(db_column='APELLIDO_DOCENTE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    idgradoseccion = models.ForeignKey('Gradoseccion', models.DO_NOTHING, db_column='ID_GRADOSECCION', blank=True, null=True)
    docente = models.CharField(db_column='ORIENTADOR',max_length=1,null=True)

    class Meta:
        managed = False
        db_table = 'docente'
    def __str__(self):
        return self.nombre_docente + ' ' + self.apellido_docente


class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(db_column='ID_EVALUACION', primary_key=True)  # Field name made lowercase.
    id_categoria = models.ForeignKey(Categoria, models.DO_NOTHING, db_column='ID_CATEGORIA', blank=True, null=True)  # Field name made lowercase.
    id_gradoseccionmateria = models.ForeignKey('Gradoseccionmateria', models.DO_NOTHING, db_column='ID_GRADOSECCIONMATERIA', blank=True, null=True)  # Field name made lowercase.
    id_trimestre = models.ForeignKey('Trimestre', models.DO_NOTHING, db_column='ID_TRIMESTRE', blank=True, null=True)  # Field name made lowercase.
    nombre_evaluacion = models.CharField(db_column='NOMBRE_EVALUACION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    porcentaje = models.IntegerField(db_column='PORCENTAJE', blank=True, null=False)  # Field name made lowercase.
    estado = models.IntegerField(db_column='ESTADO')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'evaluacion'
    def __str__(self):
        return self.nombre_evaluacion
    

class Evaluacionalumno(models.Model):
    id_evaluacionalumno = models.AutoField(db_column='ID_EVALUACIONALUMNO', primary_key=True)  # Field name made lowercase.
    id_evaluacion = models.ForeignKey(Evaluacion, models.DO_NOTHING, db_column='ID_EVALUACION', blank=True, null=True)  # Field name made lowercase.
    id_alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='ID_ALUMNO', blank=True, null=True)  # Field name made lowercase.
    nota = models.FloatField(db_column='NOTA',blank=True,null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evaluacionalumno'



class Grado(models.Model):
    id_grado = models.AutoField(db_column='ID_GRADO', primary_key=True)  # Field name made lowercase.
    grado = models.CharField(db_column='GRADO', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'grado'
    def __str__(self):
        return self.grado


class Gradoseccion(models.Model):
    id_gradoseccion = models.AutoField(db_column='ID_GRADOSECCION', primary_key=True)  # Field name made lowercase.
    id_grado = models.ForeignKey(Grado, models.DO_NOTHING, db_column='ID_GRADO', blank=True, null=True)  # Field name made lowercase.
    id_seccion = models.ForeignKey('Seccion', models.DO_NOTHING, db_column='ID_SECCION', blank=True, null=True)  # Field name made lowercase.
    turno_gradoseccion = models.CharField(db_column='TURNO_GRADOSECCION', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gradoseccion'
    def __str__(self):
        return self.id_grado.grado + ' ' + self.id_seccion.seccion


class Gradoseccionmateria(models.Model):
    id_gradoseccionmateria = models.AutoField(db_column='ID_GRADOSECCIONMATERIA', primary_key=True)  # Field name made lowercase.
    id_gradoseccion = models.ForeignKey(Gradoseccion, models.DO_NOTHING, db_column='ID_GRADOSECCION', blank=True, null=True)  # Field name made lowercase.
    id_materia = models.ForeignKey('Materia', models.DO_NOTHING, db_column='ID_MATERIA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'gradoseccionmateria'
    def __str__(self):
        return self.id_gradoseccion.id_grado.grado + ' ' + self.id_gradoseccion.id_seccion.seccion + ' ' + self.id_materia.nombre_materia


class Materia(models.Model):
    id_materia = models.AutoField(db_column='ID_MATERIA', primary_key=True)  # Field name made lowercase.
    id_docente = models.ForeignKey(Docente, models.DO_NOTHING, db_column='ID_DOCENTE', blank=True, null=True)  # Field name made lowercase.
    nombre_materia = models.CharField(db_column='NOMBRE_MATERIA', max_length=100, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'materia'
    def __str__(self):
        return self.nombre_materia + '|' + self.id_docente.nombre_docente + ' ' + self.id_docente.apellido_docente


class Seccion(models.Model):
    id_seccion = models.AutoField(db_column='ID_SECCION', primary_key=True)  # Field name made lowercase.
    seccion = models.CharField(db_column='SECCION', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'seccion'
    def __str__(self):
        return self.seccion


class Trimestre(models.Model):
    id_trimestre = models.AutoField(db_column='ID_TRIMESTRE', primary_key=True)  # Field name made lowercase.
    trimestre = models.CharField(db_column='TRIMESTRE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    anio = models.CharField(db_column='ANIO', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'trimestre'
    def __str__(self):

        return self.trimestre + ' Año ' + self.anio

    
    def clean(self):
        # Validar que no se repita el nombre del trimestre en el mismo año
        trimestres_mismo_anio = Trimestre.objects.filter(anio=self.anio, trimestre=self.trimestre)
        if trimestres_mismo_anio.exists():
            raise ValidationError('El nombre del trimestre ya existe en el mismo año.')
    
class Promediomateria(models.Model):
    id_alumno = models.OneToOneField(Alumno, models.DO_NOTHING, db_column='ID_ALUMNO', primary_key=True)  # Field name made lowercase.
    id_materia = models.ForeignKey(Materia, models.DO_NOTHING, db_column='ID_MATERIA')  # Field name made lowercase.
    id_trimestre = models.ForeignKey('Trimestre', models.DO_NOTHING, db_column='ID_TRIMESTRE')  # Field name made lowercase.
    promedio = models.FloatField(db_column='PROMEDIO', blank=True, null=True)  # Field name made lowercase.
    observacion = models.CharField(db_column='OBSERVACION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fecha_edicion = models.DateField(db_column='FECHA_EDICION', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'promediomateria'
        unique_together = (('id_alumno', 'id_materia', 'id_trimestre'),)    


