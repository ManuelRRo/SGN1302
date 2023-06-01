from django.shortcuts import render,redirect
from .models import Evaluacion,Evaluacionalumno,Alumno,Gradoseccion,Docente,Materia,Gradoseccionmateria
from .forms import EvaluacionForm,EvaluacionAlumnoForm,DocenteForm
from aplicaciones.usuarios.forms import RegisterUserForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@login_required()
def home(request):
    context = {}
    usuarios = User.objects.all()
    for usuario in usuarios:
        docente = Docente.objects.filter(nombre_docente=usuario.first_name,apellido_docente=usuario.last_name)
    try:
        idmateria = Materia.objects.get(id_docente=docente[0].id_docente)
        context["gradsec"] = Gradoseccionmateria.objects.filter(id_materia=idmateria.id_materia)
    except ObjectDoesNotExist:
        print("no hay materias ingresadas")

    return render (request,'home/inicio.html',context)

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

class ListarEvaluacionesAlumnos(View):
    model = Evaluacionalumno
    form_class = EvaluacionAlumnoForm
    template_name = 'estudiante/listar-evas-alumnos.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self,**kwargs):
        contexto = {}
        # pone un nuevo elemento en el diccionario
        # y enviar el queryset defino en get_queryset
        #aqui puedo agregar mas modelos a enviar a la vista
        contexto['estudiantes'] = self.get_queryset()
        #pasar un formulario al contexto de la vista
        contexto['form'] = self.form_class
        return contexto

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())
    
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sgn_app:list_evas_not')
        
class ActualizarEvaluacionesAlumno(UpdateView):
    model = Evaluacionalumno
    form_class = EvaluacionAlumnoForm
    #usar mismo template para que lo carge en el form
    template_name = 'estudiante/listar-evas-alumnos.html'
    success_url = reverse_lazy('sgn_app:list_evas_not')
    #esto permite seguir manteniendo lista estudiantes aun cuando se actualiza
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['estudiantes'] = Evaluacionalumno.objects.all
        return context
#HU-01 Listar grados asignados
class ListarEvaluacionesGrados(ListView):
    model = Evaluacion
    context_object_name = 'evas'
    template_name = 'evaluacion/evaluacion.html'
    
    def get_queryset(self):
        #self.idgrado = get_object_or_404(Evaluacion,id_gradoseccionmateria_id=self.kwargs["idgrado"])
        #print()
        self.idgrado = self.kwargs["idgrado"]
        if self.idgrado!=None:
            return self.model.objects.filter(id_gradoseccionmateria=self.idgrado)
        return self.model.objects.all()

# Gestión de Docentes:
class ListarDocentes(ListView):
    model = Docente
    template_name = 'docente/listar_docentes.html'
    context_object_name = 'docentes'
    queryset = model.objects.all()


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










