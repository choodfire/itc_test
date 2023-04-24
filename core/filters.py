import django_filters
from django_filters import FilterSet
from .models import *
from .consts import STATUS_CHOICES


class ApplicantFilter(FilterSet):
    middle_name = django_filters.CharFilter(field_name='middle_name', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    phone = django_filters.NumberFilter(field_name='phone', lookup_expr='exact')
    birthday = django_filters.DateFilter(field_name='birthday', lookup_expr='exact')

    class Meta:
        model = Applicant
        fields = ['middle_name', 'first_name', 'last_name', 'phone', 'birthday']


class AppealFilter(FilterSet):
    middle_name = django_filters.CharFilter(field_name='applicant__middle_name', lookup_expr='icontains')
    first_name = django_filters.CharFilter(field_name='applicant__first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='applicant__last_name', lookup_expr='icontains')
    service_code = django_filters.CharFilter(field_name='emergency_services__service_code', lookup_expr='exact')
    status = django_filters.ChoiceFilter(field_name='status', choices=STATUS_CHOICES)

    class Meta:
        model = Appeal
        fields = ['middle_name', 'first_name', 'last_name', 'service_code', 'status']
