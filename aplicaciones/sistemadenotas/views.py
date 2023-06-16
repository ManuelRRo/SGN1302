
from django.shortcuts import get_object_or_404, render, redirect
#from .models import Evaluacion, Evaluacionalumno, Alumno, Gradoseccion, Docente, Materia, Gradoseccionmateria
from django.shortcuts import render,redirect
from .models import Evaluacion,Evaluacionalumno,Alumno,Gradoseccion,Docente,Materia,Gradoseccionmateria,Trimestre,Promediomateria
from .forms import EvaluacionForm,EvaluacionAlumnoForm,DocenteForm,AlumnoForm,TrimestreActualizarForm,EvaluacionEditarForm, TrimestreForm
from aplicaciones.usuarios.forms import RegisterUserForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View,TemplateView
from django.urls import reverse_lazy
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
    #context_object_name = 'evas'
    template_name = 'evaluacion/evaluacion.html'
    
    def get_queryset(self):
        self.idgrado = self.kwargs["idgrado"]
        if self.idgrado!=None:
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
    


#VISTAS HU-03 y HU-09
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
        self.alumnos = Evaluacionalumno.objects.filter(id_evaluacion=self.evaluacion)
        return self.alumnos

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['estudiantes'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())
    
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            try:
                idevaluacion = request.POST['idEvaluacion']
                print(idevaluacion)
                self.Evaluacion = Evaluacion.objects.get(id_evaluacion=idevaluacion)
                idAlumno = request.POST.get('idAlumno', None)
                nota = request.POST['nota']
                if idAlumno is not None and idAlumno != '':
                    self.Alumno = Alumno.objects.get(id_alumno=idAlumno)
                    self.EvaluacionAlumno = Evaluacionalumno.objects.get(id_evaluacion=self.Evaluacion, id_alumno=self.Alumno)
                    self.EvaluacionAlumno.nota = nota
                    self.EvaluacionAlumno.save()
                
            except Exception:
                messages.error(request, 'Ocurrio un error')
                
        # ID de evaluación que deseas pasar a la URL
        return redirect('sgn_app:list_evas_not', idEvaluacion=idevaluacion)


# HU-07: Mostrar Notas de Alumnos de todas las evaluaciones 
# Mostrarse baso en el archivo de excel que proporcionaron en el centro escolar.
def ver_Promedios(request, idgrado, idtrimestre):
    gradoseccion = Gradoseccionmateria.objects.get(id_gradoseccionmateria =idgrado)
    alumnos = Alumno.objects.filter(id_gradoseccion=gradoseccion.id_gradoseccion)
    evaluacionalumno = Evaluacionalumno.objects.filter(id_alumno__id_gradoseccion=gradoseccion.id_gradoseccion, id_evaluacion__id_trimestre=idtrimestre).order_by('id_evaluacion')
    evaluacion_ids = evaluacionalumno.values_list('id_evaluacion', flat=True)
    evaluaciones = Evaluacion.objects.filter(id_evaluacion__in=evaluacion_ids).filter(id_trimestre = idtrimestre)
    materia = Materia.objects.get(id_materia= gradoseccion.id_materia.id_materia)
    trimestre = Trimestre.objects.get(id_trimestre = idtrimestre)

    promedios = []
    for alumno in alumnos:
        notas = []
        for evaluacion in evaluaciones:
            evaluacion_alumno = evaluacionalumno.filter(id_alumno=alumno, id_evaluacion=evaluacion).first()
            if evaluacion_alumno:
                nota_ponderada = evaluacion_alumno.nota * (evaluacion.porcentaje / 100)
                notas.append(nota_ponderada)
        promedio = round(sum(notas), 2)
        promedios.append({'alumno': alumno, 'promedio': promedio})
   
    contexto = {
        'gradoseccion': gradoseccion,
        'evaluaciones': evaluaciones,
        'evaluacionesalumno': evaluacionalumno,
        'materia':materia,
        'trimestre': trimestre,
        'alumnos':alumnos,
        'promedios': promedios,
    }
    return render(request,'calificaciones/verPromedios.html ',contexto)

   
# Codigo HU-08 Generar archivo de excel de notas trimestrales 
class ReporteDeNotasExcel(TemplateView):
    def post(self, request, *args, **kwargs):
        # Obtiene los valores enviados desde el formulario
        comentarios = {}
        valores_promedio = {}
        grado = request.POST.get('grado','')
        trimestre = request.POST.get('trimestre','')

        for key, value in request.POST.items():
            if key.startswith('opcional_'):
                alumno_id = key.replace('opcional_', '')
                comentarios[alumno_id] = value
            elif key.startswith('promedio_'):
                alumno_id = key.replace('promedio_', '')
                valores_promedio[alumno_id] = value
                
        
        for alumno_id, valor in comentarios.items():
            # Accede a los valores por el ID del alumno
            alumno = Alumno.objects.get(id_alumno=alumno_id)

        for alumno_id, valor in valores_promedio.items():
            # Accede a los valores por el ID del alumno
            alumno = Alumno.objects.get(id_alumno=alumno_id)

        # Código para generar y devolver el archivo Excel
        return self.get(request, comentarios=comentarios, trimestre=trimestre, grado = grado ,valores_promedio=valores_promedio, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comentarios = kwargs.get('comentarios')  # Obtén los valores opcionales de los argumentos de la vista
        notas_finales = kwargs.get('valores_promedio')
        trimestre = kwargs.get('trimestre')
        grado = kwargs.get('grado')

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

        cont = 2
        numero = 1

        for alumno in alumnos:
            ws.cell(row=cont, column=1).value = int(alumno.nie) 
            alumno_id = str(alumno.id_alumno)
            if alumno_id in notas_finales:
                nota_final = notas_finales[alumno_id]
                ws.cell(row=cont, column=2).value = float(nota_final) 
            ws.cell(row=cont, column=3).value = datetime.now().strftime('%d/%m/%Y')
            alumno_id = str(alumno.id_alumno)
            if alumno_id in comentarios:
                comentario = comentarios[alumno_id]
                ws.cell(row=cont, column=4).value = comentario
            else:
                ws.cell(row=cont, column=4).value = ""
            cont += 1
            numero += 1

        nombre_archivo = "Notas " + grado +" "+ trimestre+".xlsx" 
        response = HttpResponse(content_type="application/ms-excel")
        content = "attachment; filename={0}".format(nombre_archivo)
        response['Content-Disposition'] = content
        wb.save(response)
        return response

#HU10 Cambiar Rol de Usuario
class cambiarRolListView(ListView):
    model = Docente
    template_name = 'docente/cambiar_Rol.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


def Cambiar_Rol(request,nombreUsuario):
    try:
        # Recupera el registro por el nombre de usuario
        registro = User.objects.get(username=nombreUsuario)
        
        # Cambia el estado is_superuser 
        registro.is_superuser = not registro.is_superuser
        registro.save()
    except User.DoesNotExist:
        pass
    return redirect('/cambiar_Rol/')


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
            id_gradoseccion = id
         )
        print(alumnos)
        return alumnos


def habilitar(request,id,idAlumno):
    alumno = Alumno.objects.get(id_alumno = idAlumno)
    alumno.estado = "1"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


def deshabilitar(request,id,idAlumno):
    alumno = Alumno.objects.get(id_alumno = idAlumno)
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
            id_gradoseccion = id
        )
        print(alumnos)
        return alumnos


def habilitar(request,id,idAlumno):
    alumno = Alumno.objects.get(id_alumno = idAlumno)
    alumno.estado = "1"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


def deshabilitar(request,id,idAlumno):
    alumno = Alumno.objects.get(id_alumno = idAlumno)
    alumno.estado = "0"
    alumno.save()
    return redirect(f'/habilitarDeshabilitarAlumno/{id}/')


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
    
    def post(self,request,*args,**kwargs):
        if request.method == 'POST':
            opcion = request.POST['operacion']
            # Al ser la operacion un 1
            # Se crea un registro
            if opcion == '1':
                try:
                    id_grado_seccion = request.POST.get('idGradoSeccion', None)
                    id_docente = request.POST.get('idDocente', None)
                    nombre_materia = request.POST.get('nombreMateria', None)
                    existe_materia = Materia.objects.filter(nombre_materia = nombre_materia, id_docente_id = id_docente).exists()
                    if existe_materia:
                        materias = Materia.objects.filter(nombre_materia = nombre_materia, id_docente_id = id_docente)
                        existencia_grado_seccion_materia = Gradoseccionmateria.objects.filter(id_materia__in = materias, id_gradoseccion_id = id_grado_seccion).exists()
                        if existencia_grado_seccion_materia:
                            messages.error(request,'No fue posible registrarlo porque se encontró un coincidencia en la base de datos')
                        else:
                            materia = Materia.objects.create(
                                id_docente_id = id_docente,
                                nombre_materia = nombre_materia
                            )
                            
                            Gradoseccionmateria.objects.create(
                                id_gradoseccion_id=id_grado_seccion,
                                id_materia = materia
                            )
                    else:
                        materia = Materia.objects.create(
                                id_docente_id = id_docente,
                                nombre_materia = nombre_materia
                            )
                            
                        Gradoseccionmateria.objects.create(
                            id_gradoseccion_id=id_grado_seccion,
                            id_materia = materia
                        )   
                except Exception:
                    messages.error(request, 'Ocurrio un error, introduzca datos válidos')
            else:
                # Al no ser lo anterior
                # Se edita un registro
                m=0

        # ID de evaluación que deseas pasar a la URL
        return redirect('sgn_app:asignar_clases')


# Elimina la asignación seleccionada, que anteriormente
# se puedo crear en la clase AsignacionClases 
def EliminarAsigacionClases(request, id):
    try:
        grado_seccion_materia = Gradoseccionmateria.objects.get(id_gradoseccionmateria = id)
        grado_seccion_materia.delete()
        materia = Materia.objects.get(id_materia = grado_seccion_materia.id_materia)
        materia.delete()
        
    except Exception:
        messages.error(request,'No es posible eliminar este registro')
    
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
    
    def get(self,request ,*args, **kwargs):
        return render(request,self.template_name,self.get_context_data())
    
    def post(self,request ,*args, **kwargs):
        form_teacher = self.form_teacher(request.POST)
        form_user = self.form_user(request.POST)
        if form_teacher.is_valid() and form_user.is_valid():
            form_teacher.save()
            form_user.save()
            return redirect('sgn_app:listado_docentes')
        else:
            messages.error(request, 'Ocurrio un error')
            return render(request,self.template_name,self.get_context_data())


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
    return render(request, 'docente/editar_docente.html', {'docente_form':form_teacher,'user_form':form_user})


#HU-31: Habilitar/Deshabilitar Docentes
#Vista para deshabilitar usuario
@login_required()
def deshabilitar_usuario(request, id):
    user = get_object_or_404(User, username=id)
    # Deshabilitar el usuario
    user.is_active = False
    user.save()
    return redirect('sgn_app:listado_docentes')


#Vista para habilitar usuario
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
        else: messages.error(request, "El nombre del trimestre ya existe en el mismo año.")
    return render(request, 'trimestre/crear_trimestre.html', {'form_trimestre':form_trimestre})


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
        messages.error(request, "No se puede eliminar el trimestre porque existen registros dependientes.")
    return redirect ('sgn_app:listar_trimestres')
    

# HU-38: Agregar Evaluación
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


# HU-40: Editar Evaluación
class EvaluacionEditar(UpdateView):
    model = Evaluacion
    template_name = "evaluacion/editarEvaluacion.html"
    form_class = EvaluacionEditarForm
    success_url = reverse_lazy('sgn_app:correcto')

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


    

