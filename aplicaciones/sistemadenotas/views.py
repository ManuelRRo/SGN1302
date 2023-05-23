from django.shortcuts import render,redirect
from .models import Evaluacion,Evaluacionalumno,Alumno,Gradoseccion
from .forms import EvaluacionForm,EvaluacionAlumnoForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def home(request):
    return render (request,'home/inicio.html',{})

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











