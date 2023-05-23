from django.shortcuts import render,redirect
from .models import Evaluacion,Evaluacionalumno,Alumno,Gradoseccion
from .forms import EvaluacionForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def home(request):
    return render (request,'home/inicio.html',{})

#VISTAS HU-03 
def CrearEvaluacionAlumno(request):
    submitted = False
    if request.method == "POST":
        #form = EvaluacionForm(request.POST)
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save() #contiene los datos de la evaluacion que se acaba de crear
            #grado = form.cleaned_data['id_gradoseccionmateria'].id_gradoseccion.id_gradoseccion
            print(evaluacion)
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




