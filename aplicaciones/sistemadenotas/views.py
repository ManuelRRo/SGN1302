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

# HU_01 Listar Grados asignados | Materias impartidas
# Posee dos comportamientos:
#   - Rol profesor -> cumple HU-01
#   - Rol Administrador -> no se ejecuta HU-01
@login_required
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

#VISTAS HU-03 o HU-09
def CrearEvaluacionAlumno(request):
    submitted = False
    if request.method == "POST":
        #form = EvaluacionForm(request.POST)
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save() #contiene los datos de la evaluacion que se acaba de crear
            #grado = form.cleaned_data['id_gradoseccionmateria'].id_gradoseccion.id_gradoseccion
            if evaluacion is not None:
                grado = evaluacion.id_gradoseccionmateria.id_gradoseccion.id_gradoseccion
                alumno = Alumno.objects.filter(id_gradoseccion=grado)
                for e in alumno:
                    evaalumno = Evaluacionalumno.objects.create(id_evaluacion = evaluacion,id_alumno = e,nota = 0.0)
                return HttpResponseRedirect('/estudiante/crear-eva-est?submitted=True')
    else:
        form = EvaluacionForm
        # USER SUBMITTER THE FORM
        if 'submitted' in request.GET:
            submitted = True
    context = {
        'form':form, 
        'submitted':submitted,
    }
    return render(request,'estudiante/crear-evaluacion.html',context)


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

    def get_context_data(self,**kwargs):
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
                    i = 0
                else:
                    # Mostrar mensaje de error o realizar alguna otra acción
                    # ...
                    m = 0
            except Exception:
                messages.error(request, 'Ocurrio un error')
                
        # ID de evaluación que deseas pasar a la URL
        return redirect('sgn_app:list_evas_not', idEvaluacion=idevaluacion)


# Gestión de Docentes: 
# HU-32 Listar Docentes
class ListarDocentes(ListView):
    model = Docente
    template_name = 'docente/listar_docentes.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()


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
    


class ListarDocentes(ListView):
    model = Docente
    template_name = 'docente/listar_docentes.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()



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

