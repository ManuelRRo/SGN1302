
from django.shortcuts import get_object_or_404, render, redirect
from .models import Evaluacion, Evaluacionalumno, Alumno, Gradoseccion, Docente, Materia, Gradoseccionmateria
from django.shortcuts import render,redirect
from .models import Evaluacion,Evaluacionalumno,Alumno,Gradoseccion,Docente,Materia,Gradoseccionmateria,Trimestre
from .forms import EvaluacionForm,EvaluacionAlumnoForm,DocenteForm,AlumnoForm,TrimestreActualizarForm,EvaluacionEditarForm
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


# HU_01 Listar Grados asignados | Materias impartidas
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
        context["gradsec"] = Gradoseccionmateria.objects.filter(id_materia__in=materia)
    
    return render (request,'home/inicio.html',context)


# HU-02 Listar Evaluaciones de Grado
# De acuerdo a la materia seleccionada de ese grado
class ListarEvaluacionesGrados(ListView):
    model = Evaluacion
    context_object_name = 'evas'
    template_name = 'evaluacion/evaluacion.html'
    
    def get_queryset(self):
        self.idgrado = self.kwargs["idgrado"]
        if self.idgrado!=None:
            return self.model.objects.filter(id_gradoseccionmateria=self.idgrado)
        return self.model.objects.all()

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

# Permite listar los alumnos de esta evalucion
# a la vez actualizar
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


class ActualizarEvaluacionesAlumno(UpdateView):
    model = Evaluacionalumno
    form_class = EvaluacionAlumnoForm
    # usar mismo template para que lo carge en el form
    template_name = 'estudiante/listar-evas-alumnos.html'
    success_url = reverse_lazy('sgn_app:list_evas_not')
    # esto permite seguir manteniendo lista estudiantes aun cuando se actualiza

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = Evaluacionalumno.objects.all
        return context


# HU-01 Listar grados asignados
class ListarEvaluacionesGrados(ListView):
    model = Evaluacion
    context_object_name = 'evas'
    template_name = 'evaluacion/evaluacion.html'

    def get_queryset(self):
        # self.idgrado = get_object_or_404(Evaluacion,id_gradoseccionmateria_id=self.kwargs["idgrado"])
        # print()
        self.idgrado = self.kwargs["idgrado"]
        if self.idgrado != None:
            return self.model.objects.filter(id_gradoseccionmateria=self.idgrado)
        return self.model.objects.all()

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


@login_required()
def deshabilitar_usuario(request, id):
    user = get_object_or_404(User, username=id)
    # Deshabilitar el usuario
    user.is_active = False
    user.save()
    return redirect('sgn_app:listado_docentes')


@login_required()
def habilitar_usuario(request, id):
    user = get_object_or_404(User, username=id)
    # Deshabilitar el usuario
    user.is_active = True
    user.save()
    return redirect('sgn_app:listado_docentes')  


class Correcto(TemplateView):
    template_name = "trimestre/correcto.html"


class ActualizarTrimestre(UpdateView):
    model = Trimestre
    template_name = "trimestre/actualizarTrim.html"
    form_class = TrimestreActualizarForm
    success_url = reverse_lazy('sgn_app:correcto')
    

class EvaluacionEditar(UpdateView):
    model = Evaluacion
    template_name = "evaluacion/editarEvaluacion.html"
    form_class = EvaluacionEditarForm
    success_url = reverse_lazy('sgn_app:correcto')


#HU-21
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


def ver_Evaluaciones(request, idgrado):
    gradoseccion = Gradoseccionmateria.objects.get(id_gradoseccionmateria =idgrado)
    alumnos = Alumno.objects.filter(id_gradoseccion=gradoseccion.id_gradoseccion)
    #evaluaciones = Evaluacion.objects.filter(id_gradoseccionmateria = gradoseccion.id_gradoseccionmateria)
    
    alumno_ids = alumnos.values_list('id_alumno', flat=True)
    evaluacionalumno = Evaluacionalumno.objects.filter(id_alumno__in=alumno_ids).order_by('id_evaluacion')
    evaluacion_ids = evaluacionalumno.values_list('id_evaluacion', flat=True)
    evaluaciones = Evaluacion.objects.filter(id_evaluacion__in=evaluacion_ids)
    materia = Materia.objects.get(id_materia= gradoseccion.id_materia.id_materia)
    trimestre = Trimestre.objects.filter(evaluacion__id_trimestre__isnull=False).first()

    #print(evaluaciones)


    #alumnos = Alumno.objects.all()

    print(evaluaciones)
    contexto = {
        'gradoseccion': gradoseccion,
        'evaluaciones': evaluaciones,
        'evaluacionesalumno': evaluacionalumno,
        'materia':materia,
        'trimestre': trimestre,
        'alumnos':alumnos
    }
    return render(request,'calificaciones/verPromedios.html ',contexto)