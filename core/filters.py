import django_filters
from django_filters import FilterSet
from .models import *


class ApplicantFilter(FilterSet):
    full_name = django_filters.CharFilter(field_name='full_name', lookup_expr='icontains')
    phone = django_filters.NumberFilter(field_name='phone', lookup_expr='exact')
    birthday = django_filters.DateFilter(field_name='birthday', lookup_expr='exact')

    class Meta:
        model = Applicant
        fields = ['full_name', 'phone', 'birthday']


class AppealFilter(FilterSet):
    full_name = django_filters.CharFilter(field_name='applicant__full_name', lookup_expr='icontains')
    service_code = django_filters.CharFilter(field_name='emergency_service__service_code', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Appeal
        fields = ['full_name', 'service_code', 'status']
