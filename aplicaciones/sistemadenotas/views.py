
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from .models import Evaluacion, Evaluacionalumno, Alumno, Gradoseccion, Docente, Materia, Gradoseccionmateria
from django.shortcuts import render, redirect
from .models import Evaluacion, Evaluacionalumno, Alumno, Gradoseccion, Docente, Materia, Gradoseccionmateria, Trimestre, Promediomateria
from .forms import EvaluacionForm, EvaluacionAlumnoForm, DocenteForm, AlumnoForm, TrimestreActualizarForm, EvaluacionEditarForm, TrimestreForm
from aplicaciones.usuarios.forms import RegisterUserForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from openpyxl import Workbook
from django.http.response import HttpResponse
from aplicaciones.sistemadenotas.filters import EvaluacionFilter
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO
import base64
from asgiref.sync import sync_to_async
from django.db.models import Count, Q 
from operator import itemgetter




# HU-01 Listar Grados asignados | Materias impartidas
# Posee dos comportamientos:
#   - Rol profesor -> cumple HU-01
#   - Rol Administrador -> no se ejecuta HU-01
@login_required()
def home(request):
    context = {}
    # Al no ser admin se cumple la HU-01
    if not request.user.is_superuser:
        docente = Docente.objects.get(numidentificacion=request.user.username)
        materia = Materia.objects.filter(id_docente=docente)
        grado_seccion_materia = Gradoseccionmateria.objects.filter(id_materia__in=materia)
        gradoseccion = Gradoseccion.objects.filter(gradoseccionmateria__id_materia__id_docente=docente).distinct()
        context['grado_seccion'] = gradoseccion
        context["grado_seccion_materia"] = grado_seccion_materia
    
    return render (request,'home/inicio.html',context)


# HU-02 Listar Evaluaciones de Grado
# De acuerdo a la materia seleccionada de ese grado
class ListarEvaluacionesGrados(ListView):
    model = Evaluacion
    # context_object_name = 'evas'
    template_name = 'evaluacion/evaluacion.html'

    def get_queryset(self):
        self.idgrado = self.kwargs["idgrado"]
        if self.idgrado != None:
            return self.model.objects.filter(id_gradoseccionmateria=self.idgrado)
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluacion_filter = EvaluacionFilter(self.request.GET,queryset = self.get_queryset())
        # Semejante al home: para el navbar
        docente = Docente.objects.get(numidentificacion=self.request.user.username)
        materia = Materia.objects.filter(id_docente=docente)
        grado_seccion_materia = Gradoseccionmateria.objects.filter(id_materia__in=materia)
        gradoseccion = Gradoseccion.objects.filter(gradoseccionmateria__id_materia__id_docente=docente).distinct()
        # ------------------------------------
        context["filter_form"] = evaluacion_filter.form
        context["evas"] = evaluacion_filter.qs
        context['grado_seccion'] = gradoseccion
        context["grado_seccion_materia"] = grado_seccion_materia 
        return context


# VISTAS HU-03 y HU-09
def CrearEvaluacionAlumno(request):
    submitted = False
    if request.method == "POST":
        # form = EvaluacionForm(request.POST)
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save()  # contiene los datos de la evaluacion que se acaba de crear
            # grado = form.cleaned_data['id_gradoseccionmateria'].id_gradoseccion.id_gradoseccion
            if evaluacion is not None:
                grado = evaluacion.id_gradoseccionmateria.id_gradoseccion.id_gradoseccion
                alumno = Alumno.objects.filter(id_gradoseccion=grado)
                for e in alumno:
                    evaalumno = Evaluacionalumno.objects.create(
                        id_evaluacion=evaluacion, id_alumno=e, nota=0.0)
                return HttpResponseRedirect('/estudiante/crear-eva-est?submitted=True')
    else:
        form = EvaluacionForm
        # USER SUBMITTER THE FORM
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'estudiante/crear-evaluacion.html', context)


# HU-04 - HU-05

# Permite listar los alumnos de esta evalucion
# a la vez actualizar y registrar
class ListarEvaluacionesAlumnos(View):
    model = Evaluacionalumno
    form_class = EvaluacionAlumnoForm
    template_name = 'estudiante/listar-evas-alumnos.html'

    def get_queryset(self):
        self.evaluacion = self.kwargs["idEvaluacion"]
        self.alumnos = Evaluacionalumno.objects.filter(
            id_evaluacion=self.evaluacion)
        return self.alumnos

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['estudiantes'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                idevaluacion = request.POST['idEvaluacion']
                print(idevaluacion)
                self.Evaluacion = Evaluacion.objects.get(
                    id_evaluacion=idevaluacion)
                idAlumno = request.POST.get('idAlumno', None)
                nota = request.POST['nota']
                if idAlumno is not None and idAlumno != '':
                    self.Alumno = Alumno.objects.get(id_alumno=idAlumno)
                    self.EvaluacionAlumno = Evaluacionalumno.objects.get(
                        id_evaluacion=self.Evaluacion, id_alumno=self.Alumno)
                    self.EvaluacionAlumno.nota = nota
                    self.EvaluacionAlumno.save()
            except Exception:
                messages.error(request, 'Ocurrio un error')

        # ID de evaluación que deseas pasar a la URL
        return redirect('sgn_app:list_evas_not', idEvaluacion=idevaluacion)


# HU-07: Mostrar Notas de Alumnos de todas las evaluaciones
# Mostrarse baso en el archivo de excel que proporcionaron en el centro escolar.
def ver_Promedios(request, idgrado, idtrimestre):
    gradoseccion = Gradoseccionmateria.objects.get(
        id_gradoseccionmateria=idgrado)
    alumnos = Alumno.objects.filter(
        id_gradoseccion=gradoseccion.id_gradoseccion)
    evaluacionalumno = Evaluacionalumno.objects.filter(
        id_alumno__id_gradoseccion=gradoseccion.id_gradoseccion, id_evaluacion__id_trimestre=idtrimestre).order_by('id_evaluacion')
    evaluacion_ids = evaluacionalumno.values_list('id_evaluacion', flat=True)
    evaluaciones = Evaluacion.objects.filter(
        id_evaluacion__in=evaluacion_ids).filter(id_trimestre=idtrimestre)
    materia = Materia.objects.get(
        id_materia=gradoseccion.id_materia.id_materia)
    trimestre = Trimestre.objects.get(id_trimestre=idtrimestre)

    promedios = []
    for alumno in alumnos:
        notas = []
        for evaluacion in evaluaciones:
            evaluacion_alumno = evaluacionalumno.filter(
                id_alumno=alumno, id_evaluacion=evaluacion).first()
            if evaluacion_alumno:
                nota_ponderada = evaluacion_alumno.nota * \
                    (evaluacion.porcentaje / 100)
                notas.append(nota_ponderada)
        promedio = round(sum(notas), 2)
        promedios.append({'alumno': alumno, 'promedio': promedio})

    contexto = {
        'gradoseccion': gradoseccion,
        'evaluaciones': evaluaciones,
        'evaluacionesalumno': evaluacionalumno,
        'materia': materia,
        'trimestre': trimestre,
        'alumnos': alumnos,
        'promedios': promedios,
    }
    return render(request, 'calificaciones/verPromedios.html ', contexto)


# Codigo HU-08 Generar archivo de excel de notas trimestrales 
class ReporteDeNotasExcel(TemplateView):
    def post(self, request, *args, **kwargs):
        # Obtiene los valores enviados desde el formulario
        comentarios = {}
        valores_promedio = {}
        estados = {}
        grado = request.POST.get('grado', '')
        trimestre = request.POST.get('trimestre', '')

        for key, value in request.POST.items():
            if key.startswith('opcional_'):
                alumno_id = key.replace('opcional_', '')
                comentarios[alumno_id] = value
            elif key.startswith('promedio_'):
                alumno_id = key.replace('promedio_', '')
                valores_promedio[alumno_id] = value
            elif key.startswith('estado_'):
                alumno_id = key.replace('estado_','')
                estados[alumno_id] = value

        for alumno_id, valor in comentarios.items():
            # Accede a los valores por el ID del alumno
            alumno = Alumno.objects.get(id_alumno=alumno_id)

        for alumno_id, valor in valores_promedio.items():
            # Accede a los valores por el ID del alumno
            alumno = Alumno.objects.get(id_alumno=alumno_id)
        

        # Código para generar y devolver el archivo Excel
        return self.get(request, comentarios=comentarios, trimestre=trimestre, grado=grado, valores_promedio=valores_promedio,estados = estados ,*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Obtén los valores opcionales de los argumentos de la vista
        comentarios = kwargs.get('comentarios')
        notas_finales = kwargs.get('valores_promedio')
        trimestre = kwargs.get('trimestre')
        grado = kwargs.get('grado')
        estados = kwargs.get('estados')

        alumnos = Alumno.objects.none()  # Inicializa una consulta vacía de Alumno

        for alumno_id, valor in comentarios.items():
            # Filtra los alumnos según los valores opcionales
            alumnos |= Alumno.objects.filter(id_alumno=alumno_id)
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'nie'
        ws['B1'] = 'calificacion'
        ws['C1'] = 'fecha'
        ws['D1'] = 'observacion'
        ws['E1'] = 'estado'

        cont = 2
        numero = 1

        for alumno in alumnos:
            ws.cell(row=cont, column=1).value = int(alumno.nie)
            alumno_id = str(alumno.id_alumno)
            if alumno_id in notas_finales:
                nota_final = notas_finales[alumno_id]
                ws.cell(row=cont, column=2).value = float(nota_final)
            ws.cell(row=cont, column=3).value = datetime.now().strftime(
                '%d/%m/%Y')
            alumno_id = str(alumno.id_alumno)
            if alumno_id in comentarios:
                comentario = comentarios[alumno_id]
                ws.cell(row=cont, column=4).value = comentario
            else:
                ws.cell(row=cont, column=4).value = ""
            if alumno_id in estados:
                estado = estados[alumno_id]
                ws.cell(row= cont, column = 5).value = estado
            cont += 1
            numero += 1

        nombre_archivo = "Notas " + grado + " " + trimestre+".xlsx"
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename={0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

# HU10 Cambiar Rol de Usuario


class cambiarRolListView(ListView):
    model = Docente
    template_name = 'docente/cambiar_Rol.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


def Cambiar_Rol(request, nombreUsuario):
    try:
        # Recupera el registro por el nombre de usuario
        registro = User.objects.get(username=nombreUsuario)

        # Cambia el estado is_superuser
        registro.is_superuser = not registro.is_superuser
        registro.save()
    except User.DoesNotExist:
        pass
    return redirect('/cambiar_Rol/')

#HU-15: Reporte de Alumnos Masculinos/Femeninos
def generar_grafico_barra(data, title):
    grados = list(data.keys())
    alumnos_masculinos = [item['M'] for item in data.values()]
    alumnos_femeninos = [item['F'] for item in data.values()]

    x = range(len(grados))
    width = 0.4

    plt.bar(x, alumnos_masculinos, width=width, label='Masculino')
    plt.bar([pos + width for pos in x], alumnos_femeninos, width=width, label='Femenino')

    plt.xlabel("Grados")
    plt.ylabel("Número de alumnos")
    plt.title(title)
    plt.xticks([pos + width / 2 for pos in x], grados)
    plt.legend()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()
    return image_base64

@sync_to_async
def graficos(request):
    grados_secciones = Gradoseccion.objects.filter(id_grado__in=range(1, 4), id_seccion__in=range(1, 5))
    data = []

    for gradoseccion in grados_secciones:
        gradoseccion_text = f"{gradoseccion.id_grado.grado} {gradoseccion.id_seccion.seccion}"
        alumnos = Alumno.objects.filter(id_gradoseccion=gradoseccion)
        total_masculinos = alumnos.filter(sexo='M').count()
        total_femeninos = alumnos.filter(sexo='F').count()
        data.append({
            'gradoseccion': gradoseccion_text,
            'masculinos': total_masculinos,
            'femeninos': total_femeninos
        })
    data.sort(key=itemgetter('gradoseccion'))
    grados_secciones = [item['gradoseccion'] for item in data]
    masculinos = [item['masculinos'] for item in data]
    femeninos = [item['femeninos'] for item in data]

    ancho_barras = 0.2  
    posicion_barras_femeninos = [pos + ancho_barras for pos in range(len(grados_secciones))]

    
    fig = plt.figure(figsize=(12, 6))  
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1) 
    bars1 = plt.bar(grados_secciones, masculinos, width=ancho_barras, label="Masculinos")
    bars2 = plt.bar(posicion_barras_femeninos, femeninos, width=ancho_barras, label="Femeninos")
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.xticks(rotation=0)
    plt.title("Poblacion Estudiantil de Primer Ciclo")

    plt.xlabel("Grado y Sección")
    plt.ylabel("Número de alumnos")

    plt.legend(loc='upper right')  

   

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')

    fig = plt.figure(figsize=(12, 6))  
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)  
    plt.title("Poblacion Estudiantil de Segundo Ciclo")

    # Generar el segundo gráfico de barras
    grados_secciones_2 = Gradoseccion.objects.filter(id_grado__in=range(4, 7), id_seccion__in=range(1, 5))
    data_2 = []

    for gradoseccion in grados_secciones_2:
        gradoseccion_text = f"{gradoseccion.id_grado.grado} {gradoseccion.id_seccion.seccion}"
        alumnos = Alumno.objects.filter(id_gradoseccion=gradoseccion)
        total_masculinos = alumnos.filter(sexo='M').count()
        total_femeninos = alumnos.filter(sexo='F').count()
        data_2.append({
            'gradoseccion': gradoseccion_text,
            'masculinos': total_masculinos,
            'femeninos': total_femeninos
        })
    data_2.sort(key=itemgetter('gradoseccion'))
    grados_secciones_2 = [item['gradoseccion'] for item in data_2]
    masculinos_2 = [item['masculinos'] for item in data_2]
    femeninos_2 = [item['femeninos'] for item in data_2]

    ancho_barras = 0.2
    posicion_barras_femeninos_2 = [pos + ancho_barras for pos in range(len(grados_secciones_2))]

    bars1 = plt.bar(grados_secciones_2, masculinos_2, width=ancho_barras, label="Masculinos")
    bars2 = plt.bar(posicion_barras_femeninos_2, femeninos_2, width=ancho_barras, label="Femeninos")
    plt.grid(True, axis='y', linestyle='--', alpha=0.8)

    plt.xticks(rotation=0)

    plt.xlabel("Grado y Sección")
    plt.ylabel("Número de alumnos")

    plt.legend(loc='upper right')

    # Guardar el segundo gráfico como imagen y convertirla a base64
    buffer_2 = BytesIO()
    plt.savefig(buffer_2, format='png')
    buffer_2.seek(0)
    image_base64_2 = base64.b64encode(buffer_2.read()).decode('utf-8')

    plt.close()

    # Generar el tercer gráfico de barras
    fig = plt.figure(figsize=(12, 6))
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.title("Poblacion Estudiantil de Tercer Ciclo")  

    grados_secciones_3 = Gradoseccion.objects.filter(id_grado__in=range(7, 10), id_seccion__in=range(1, 5))
    data_3 = []

    for gradoseccion in grados_secciones_3:
        gradoseccion_text = f"{gradoseccion.id_grado.grado} {gradoseccion.id_seccion.seccion}"
        alumnos = Alumno.objects.filter(id_gradoseccion=gradoseccion)
        total_masculinos = alumnos.filter(sexo='M').count()
        total_femeninos = alumnos.filter(sexo='F').count()
        data_3.append({
            'gradoseccion': gradoseccion_text,
            'masculinos': total_masculinos,
            'femeninos': total_femeninos
        })
    def custom_sort_key(item):
        grado, seccion = item['gradoseccion'].rsplit(' ', 1)
        orden_grados = {"Septimo Grado": 1, "Octavo Grado": 2, "Noveno Grado": 3}
        return (orden_grados[grado], seccion)

    data_3_sorted = sorted(data_3, key=custom_sort_key)

    grados_secciones_3 = [item['gradoseccion'] for item in data_3_sorted]
    masculinos_3 = [item['masculinos'] for item in data_3_sorted]
    femeninos_3 = [item['femeninos'] for item in data_3_sorted]

    ancho_barras = 0.2
    posicion_barras_femeninos_3 = [pos + ancho_barras for pos in range(len(grados_secciones_3))]

    bars1 = plt.bar(grados_secciones_3, masculinos_3, width=ancho_barras, label="Masculinos")
    bars2 = plt.bar(posicion_barras_femeninos_3, femeninos_3, width=ancho_barras, label="Femeninos")
    plt.grid(True, axis='y', linestyle='--', alpha=0.8)

    plt.xticks(rotation=0)

    plt.xlabel("Grado y Sección")
    plt.ylabel("Número de alumnos")

    plt.legend(loc='upper right')

    # Guardar el tercer gráfico como imagen y convertirla a base64
    buffer_3 = BytesIO()
    plt.savefig(buffer_3, format='png')
    buffer_3.seek(0)
    image_base64_3 = base64.b64encode(buffer_3.read()).decode('utf-8')
    plt.title("Poblacion Estudiantil de Tercer Ciclo")  

    plt.close()

    context = {'image_base64': image_base64,'image_base64_2': image_base64_2, 'image_base64_3': image_base64_3}
    return render(request, 'administracion/graficos.html', context)



# HU-21: Insertar Alumnos
class CrearAlumno(CreateView):
    form_class = AlumnoForm
    template_name = 'estudiante/crear-alumnos.html'
    success_url = reverse_lazy('sgn_app:home')


class HabDeshabiAlumno(ListView):
    model = Alumno
    template_name = 'estudiante/hab-desh.html'

    def get_queryset(self):
        id = self.kwargs['id']
        alumnos = Alumno.objects.filter(
            id_gradoseccion=id
        )
        print(alumnos)
        return alumnos


def habilitar(request, id, idAlumno):
    alumno = Alumno.objects.get(id_alumno=idAlumno)
    alumno.estado = "1"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


def deshabilitar(request, id, idAlumno):
    alumno = Alumno.objects.get(id_alumno=idAlumno)
    alumno.estado = "0"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


# HU-23: Habilitar/Deshabilitar Alumnos
class HabDeshabiAlumno(ListView):
    model = Alumno
    template_name = 'estudiante/hab-desh.html'

    def get_queryset(self):
        id = self.kwargs['id']
        alumnos = Alumno.objects.filter(
            id_gradoseccion=id
        )
        print(alumnos)
        return alumnos


def habilitar(request, id, idAlumno):
    alumno = Alumno.objects.get(id_alumno=idAlumno)
    alumno.estado = "1"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


def deshabilitar(request, id, idAlumno):
    alumno = Alumno.objects.get(id_alumno=idAlumno)
    alumno.estado = "0"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')

# HU-22: Editar Alumno
class ActualizarAlumno(UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'estudiante/listar_alumnoGradoSeccion.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        self.gradoseccion = self.kwargs["id_gradoseccion"]
        self.alumnos = Alumno.objects.filter(id_gradoseccion=self.gradoseccion)
        context['estudiantes'] = self.alumnos
        return context
    
    def get_success_url(self):
        grado = self.kwargs['id_gradoseccion']
        url = reverse('sgn_app:ListarAlumno', kwargs={'id_gradoseccion': grado})
        return url
    
# HU-24: Listar Alumnos

class ListarAlumno(View):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'estudiante/listar_alumnoGradoSeccion.html'

    def get_queryset(self):
        self.gradoseccion = self.kwargs["id_gradoseccion"]
        self.alumnos = Alumno.objects.filter(id_gradoseccion=self.gradoseccion)
        return self.alumnos

    def get_context_data(self, **kwargs):
        contexto = {}
        # Semejante al home: para el navbar
        docente = Docente.objects.get(numidentificacion=self.request.user.username)
        materia = Materia.objects.filter(id_docente=docente)
        grado_seccion_materia = Gradoseccionmateria.objects.filter(id_materia__in=materia)
        gradoseccion = Gradoseccion.objects.filter(gradoseccionmateria__id_materia__id_docente=docente).distinct()
        # ------------------------------------
        contexto['grado_seccion'] = gradoseccion
        contexto["grado_seccion_materia"] = grado_seccion_materia
        contexto['estudiantes'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        
        return redirect('sgn_app:ListarAlumno',id_gradoseccion=self.kwargs["id_gradoseccion"])   



# ----------------------------------------------
# Gestión de Docentes:
# ----------------------------------------------

# HU-28: Asignación de Grado/Sección con Materia
# Asignación de la materia que impartira el docente en un
# determinado grado y sección
class AsignacionClases(View):
    model = Gradoseccionmateria
    template_name = 'docente/asignacion_clases.html'

    def get_queryset(self):
        consultas = {}
        consultas['grado_seccion_materia'] = self.model.objects.all()
        consultas['grado_seccion'] = Gradoseccion.objects.all()
        consultas['docentes'] = Docente.objects.all()
        return consultas

    def get_context_data(self, **kwargs):
        context = {}
        context = self.get_queryset()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            opcion = request.POST['operacion']
            # Al ser la operacion un 1
            # Se crea un registro
            if opcion == '1':
                try:
                    id_grado_seccion = request.POST.get('idGradoSeccion', None)
                    id_docente = request.POST.get('idDocente', None)
                    nombre_materia = request.POST.get('nombreMateria', None)
                    existe_materia = Materia.objects.filter(
                        nombre_materia=nombre_materia, id_docente_id=id_docente).exists()
                    if existe_materia:
                        materias = Materia.objects.filter(
                            nombre_materia=nombre_materia, id_docente_id=id_docente)
                        existencia_grado_seccion_materia = Gradoseccionmateria.objects.filter(
                            id_materia__in=materias, id_gradoseccion_id=id_grado_seccion).exists()
                        if existencia_grado_seccion_materia:
                            messages.error(
                                request, 'No fue posible registrarlo porque se encontró un coincidencia en la base de datos')
                        else:
                            materia = Materia.objects.create(
                                id_docente_id=id_docente,
                                nombre_materia=nombre_materia
                            )

                            Gradoseccionmateria.objects.create(
                                id_gradoseccion_id=id_grado_seccion,
                                id_materia=materia
                            )
                    else:
                        materia = Materia.objects.create(
                            id_docente_id=id_docente,
                            nombre_materia=nombre_materia
                        )

                        Gradoseccionmateria.objects.create(
                            id_gradoseccion_id=id_grado_seccion,
                            id_materia=materia
                        )
                except Exception:
                    messages.error(
                        request, 'Ocurrio un error, introduzca datos válidos')
            else:
                # Al no ser lo anterior
                # Se edita un registro
                m = 0

        # ID de evaluación que deseas pasar a la URL
        return redirect('sgn_app:asignar_clases')


# Elimina la asignación seleccionada, que anteriormente
# se puedo crear en la clase AsignacionClases
def EliminarAsigacionClases(request, id):
    try:
        grado_seccion_materia = Gradoseccionmateria.objects.get(id_gradoseccionmateria = id)
        materia = Materia.objects.get(id_materia = grado_seccion_materia.id_materia.id_materia)
        grado_seccion_materia.delete()
        materia.delete()

    except Exception:
        messages.error(request, 'No es posible eliminar este registro')

    return redirect('sgn_app:asignar_clases')


# HU-29 Agrega Docentes
class CrearDocentes(View):
    model = Docente
    form_teacher = DocenteForm
    form_user = RegisterUserForm
    template_name = 'docente/crear_docente.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        context['docente'] = self.get_queryset()
        context['docente_form'] = self.form_teacher
        context['user_form'] = self.form_user
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form_teacher = self.form_teacher(request.POST)
        form_user = self.form_user(request.POST)
        if form_teacher.is_valid() and form_user.is_valid():
            form_teacher.save()
            form_user.save()
            return redirect('sgn_app:listado_docentes')
        else:
            messages.error(request, 'Ocurrio un error')
            return render(request, self.template_name, self.get_context_data())


# HU-30: Editar Docentes
@login_required()
def EditarDocente(request, id):
    docente = get_object_or_404(Docente, numidentificacion=id)
    user = get_object_or_404(User, username=id)
    if request.method == 'POST':
        form_teacher = DocenteForm(request.POST, instance=docente)
        form_user = UserCreationForm(request.POST, instance=user)
        if form_teacher.is_valid() and form_user.is_valid():
            form_teacher.save()
            form_user.save()
            return redirect('sgn_app:listado_docentes')
    else:
        form_teacher = DocenteForm(instance=docente)
        form_user = RegisterUserForm(instance=user)
    return render(request, 'docente/editar_docente.html', {'docente_form': form_teacher, 'user_form': form_user})


# HU-31: Habilitar/Deshabilitar Docentes
# Vista para deshabilitar usuario
@login_required()
def deshabilitar_usuario(request, id):
    user = get_object_or_404(User, username=id)
    # Deshabilitar el usuario
    user.is_active = False
    user.save()
    return redirect('sgn_app:listado_docentes')


# Vista para habilitar usuario
@login_required()
def habilitar_usuario(request, id):
    user = get_object_or_404(User, username=id)
    # Deshabilitar el usuario
    user.is_active = True
    user.save()
    return redirect('sgn_app:listado_docentes')


# HU-32 Listar Docentes
class ListarDocentes(ListView):
    model = Docente
    template_name = 'docente/listar_docentes.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context

# ------------------------------------------





# HU-33: Crear Trimestre
def CrearTrimestre(request):
    form_trimestre = TrimestreForm(request.POST or None)
    if request.method == 'POST':
        if form_trimestre.is_valid():
            form_trimestre.save()
            return redirect('sgn_app:crear_trimestre')
        else:
            messages.error(
                request, "la combinacion trimestre año ya ha sido registrada")
    return render(request, 'trimestre/crear_trimestre.html', {'form_trimestre': form_trimestre})


class Correcto(TemplateView):
    template_name = "trimestre/correcto.html"


# HU-34: Consultar Trimestres
class ListarTrimestres(ListView):
    model = Trimestre
    template_name = 'trimestre/listar_trimestres.html'
    context_object_name = 'trimestres'
    queryset = model.objects.all()


# HU-35: Actualizar Trimestre
class ActualizarTrimestre(UpdateView):
    model = Trimestre
    template_name = "trimestre/actualizarTrim.html"
    form_class = TrimestreActualizarForm
    success_url = reverse_lazy('sgn_app:correcto')

# HU-36: Eliminar Trimestre


def EliminarTrimestre(request, id):
    try:
        trimestre = Trimestre.objects.get(id_trimestre=id)
        trimestre.delete()
    except Exception:
        messages.error(
            request, "No se puede eliminar el trimestre porque existen registros dependientes.")
    return redirect('sgn_app:listar_trimestres')


# HU-37: Listar Evaluaciones
class ListarEvaluaciones(ListView):
    model = Evaluacion
    template_name = 'evaluacion/listar_evaluaciones.html'
    context_object_name = 'evaluaciones'
    queryset = model.objects.all()

# HU-38: Agregar Evaluación
def CrearEvaluacionAlumno(request):
    submitted = False
    if request.method == "POST":
        # form = EvaluacionForm(request.POST)
        form = EvaluacionForm(request.POST)
        try:
            form_valid = form.is_valid()
        except ValueError:
            form_valid = False
        if form_valid:
            evaluacion = form.save()  # contiene los datos de la evaluacion que se acaba de crear
            # grado = form.cleaned_data['id_gradoseccionmateria'].id_gradoseccion.id_gradoseccion
            if evaluacion.id_trimestre is None:
                return HttpResponseRedirect('/estudiante/crear-eva-est')
            if evaluacion is not None :
                grado = evaluacion.id_gradoseccionmateria.id_gradoseccion.id_gradoseccion
                alumno = Alumno.objects.filter(id_gradoseccion=grado)
                for e in alumno:
                    evaalumno = Evaluacionalumno.objects.create(
                        id_evaluacion=evaluacion, id_alumno=e, nota=0.0)
                return HttpResponseRedirect('/estudiante/crear-eva-est?submitted=True')
        else:
            return HttpResponseRedirect('/estudiante/crear-eva-est')
                   
    else:
        form = EvaluacionForm
        # USER SUBMITTER THE FORM
        if 'submitted' in request.GET:
            submitted = True
        else:
            submitted = False
    context = {
        'form': form,
        'submitted': submitted,
    }
    return render(request, 'estudiante/crear-evaluacion.html', context)


# HU-40: Editar Evaluación
class EvaluacionEditar(UpdateView):
    model = Evaluacion
    template_name = "evaluacion/editarEvaluacion.html"
    form_class = EvaluacionEditarForm
    success_url = reverse_lazy('sgn_app:listar_evaluaciones')

def evaluacion_editar_docente(request,idEvaluacion):

    evaluacion = Evaluacion.objects.get(id_evaluacion = idEvaluacion)
    idgrado = evaluacion.id_gradoseccionmateria.id_gradoseccionmateria
    print(idgrado)
    if request.method == 'POST':
        id_evaluacion = request.POST['id_evaluacion']
        nombre_evaluacion = request.POST['nombre_evaluacion']
        evaluacion.nombre_evaluacion = nombre_evaluacion
        evaluacion.save()
        return redirect('sgn_app:listar_evas_grado', idgrado=idgrado)
    else:
        return render(request, 'evaluacion/editar_evaluacion_docente.html',{'evaluacion':evaluacion})


    

class IngresarRoles(ListView):
    model = Docente
    template_name = 'administracion/ingresarRoles.html'
    def get_queryset(self):
        id = self.kwargs['id']
        alumnos = Alumno.objects.filter(
            id_gradoseccion = id
         )
        print(alumnos)
        return alumnos

#class Docente(AbstractUser):
    #group, created = Group.objects.get_or_create(name='Docentes Administradores')
    #permissions = Permission.objects.filter(content_type__app_label='aplicaciones.sistemadenotas', codename__startswith='change_')
    #group.permissions.set(permissions)
    #docente = Docente.objects.get(username='nombre_de_usuario')
    #docente.groups.add(group)
    #group.save()
    #docente.save()

# Codigo HU_10 Generar archivo de excel de notas trimestrales 
class ReporteDeNotasExcel(TemplateView):
    def get(self,request,*args,**kwargs):
        alumnos = Alumno.objects.all()
        wb = Workbook()
        ws = wb.active
        ws['A1'] = 'nie'
        ws['B1'] = 'calificacion'
        ws['C1'] = 'fecha'
        ws['D1'] = 'observacion'
        ws['E1'] = 'asignatura'

        cont = 2
        numero = 1

        for alumno in alumnos:
            ws.cell(row = cont, column = 1).value = alumno.nie
            ws.cell(row = cont , column = 2).value = 10
            ws.cell(row = cont , column = 3).value = "13/06/2023"
            ws.cell(row = cont , column = 4).value = "Excelente"
            ws.cell(row = cont , column = 5).value = "AS1"
            cont+=1
            numero+1
        
        nombre_archivo = "NotasExcel.xlsx"
        response = HttpResponse(content_type = "application/ms-excel")
        content = "attachment; filename = {0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response




