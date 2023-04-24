from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
import core.filters
from .models import Appeal, Applicant, EmergencyService
from django.http import JsonResponse
from django.db.models import Avg
from .forms import *
import datetime
from .filters import *

class FirstView(TemplateView):
    template_name = 'core/first.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appeals = get_list_or_404(Appeal)
        context['lengthh'] = len(appeals)

        return context


class SecondView(TemplateView):
    template_name = 'core/second.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs['pk']
        applicant = get_object_or_404(Applicant, pk=pk)
        context['phone'] = applicant.phone

        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     pk = self.request.GET['pk']
    #     applicant = get_object_or_404(Applicant, pk=pk)
    #     context['phone'] = applicant.phone
    #
    #     return context


class ThirdView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect("https://www.google.com")


class FourthView(TemplateView):
    template_name = 'core/fourth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = f"""{self.request} \n
        {self.request.scheme} \n 
        {self.request.body} \n 
        {self.request.path} \n 
        {self.request.path_info} \n 
        {self.request.encoding} \n 
        {self.request.content_type} \n 
        {self.request.content_params} \n 
        {self.request.GET} \n 
        {self.request.POST} \n 
        {self.request.COOKIES} \n 
        {self.request.FILES} \n 
        {self.request.META} \n 
        {self.request.headers} \n 
        {self.request.resolver_match}
        """

        return context


class FifthView(TemplateView):
    template_name = 'core/fourth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = f'''Телефон = {self.request.GET['phone']}, информация = {self.request.GET['data']}'''

        return context


class SixthView(TemplateView):
    template_name = 'core/sixth.html'

    def get(self, request, *args, **kwargs):
        return JsonResponse({'data': self.request.GET.dict()})


class AppealsView(ListView):
    model = Appeal
    template_name = 'core/appeals.html'

    def get_filters(self):
        return core.filters.AppealFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    # def get_queryset(self):
    #     return Appeal.objects.all().select_related('applicant').prefetch_related('emergency_services')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average'] = Appeal.objects.aggregate(Avg('emergency_services'))['emergency_services__avg']
        context['filter'] = AppealFilter(self.request.GET)

        return context


class AppealDetailView(DetailView):
    model = Appeal
    template_name = 'core/appeal_detail.html'


class ApplicantsView(ListView):
    model = Applicant
    template_name = 'core/applicants.html'

    def get_filters(self):
        return core.filters.ApplicantFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filterr = ApplicantFilter(self.request.GET)
        context['filter'] = filterr

        return context



class ApplicantDetailView(DetailView):
    model = Applicant
    template_name = 'core/applicant_detail.html'


class ServicesView(ListView):
    model = EmergencyService
    template_name = 'core/services.html'


class ServiceDetailView(DetailView):
    model = EmergencyService
    template_name = 'core/service_detail.html'


class Index(TemplateView):
    template_name = 'core/index.html'


class AppealUpdateView(UpdateView):
    model = Appeal
    template_name = 'core/update.html'
    form_class = AppealForm

    def get_success_url(self):
        return reverse('core:appeals')


class ApplicantUpdateView(UpdateView):
    model = Applicant
    template_name = 'core/update.html'
    form_class = ApplicantForm

    def get_success_url(self):
        return reverse('core:applicants')


class ServiceUpdateView(UpdateView):
    model = EmergencyService
    template_name = 'core/update.html'
    form_class = EmergencyServiceForm

    def get_success_url(self):
        return reverse('core:services')


class ServiceCreateView(CreateView):
    form_class = EmergencyServiceForm
    template_name = 'core/create.html'
    model = EmergencyService

    def get_success_url(self):
        return reverse('core:services')


class ApplicantCreateView(CreateView):
    form_class = ApplicantForm
    template_name = 'core/create.html'
    model = Applicant

    def get_success_url(self):
        return reverse('core:applicants')


class AppealCreateView(CreateView):
    form_class = AppealForm
    template_name = 'core/create.html'
    model = Appeal

    def get_success_url(self):
        return reverse('core:appeals')
