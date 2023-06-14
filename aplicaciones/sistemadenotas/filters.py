from aplicaciones.sistemadenotas.models import Evaluacion
import django_filters


class EvaluacionFilter(django_filters.FilterSet):

    class Meta:
        model = Evaluacion
        fields = ['id_trimestre']