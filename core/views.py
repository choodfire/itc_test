from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView, DetailView, ListView, UpdateView, CreateView
import core.filters
from .models import Appeal, Applicant, EmergencyService
from django.http import JsonResponse
from django.db.models import Avg
from .forms import *
from .filters import *
from django.core import serializers


class AppealsCountView(TemplateView):
    """
    Отображает количество происшествий, 404 если их нет
    """
    template_name = 'core/first.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appeals = get_list_or_404(Appeal)
        context['length'] = len(appeals)

        return context


class ApplicantPhoneNumberView(TemplateView):
    """
    Отображает номер телефона заявителя по id, 404 если заявителя нет
    """
    template_name = 'core/second.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = kwargs['pk']
        applicant = get_object_or_404(Applicant, pk=pk)
        context['phone'] = applicant.phone

        return context


class RedirectView(TemplateView):
    """
    Перенаправляет на другую страницу
    """
    def get(self, request, *args, **kwargs):
        return redirect("https://www.google.com")


class RequestDataView(TemplateView):
    """
    Отображает данные запроса
    """
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


class ApplicantDataView(TemplateView):
    """
    Отображает данные заявителя по id
    """
    template_name = 'core/fifth.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        phone = self.request.GET['phone']

        context['applicant'] = Applicant.objects.get(phone__exact=phone)

        return context


class ApplicantDataJSONView(TemplateView):
    """
    Отображает данные заявителя по id в формате JSON
    """
    template_name = 'core/sixth.html'

    def get(self, request, *args, **kwargs):
        data = serializers.serialize('json', [Applicant.objects.get(id=kwargs['pk'])])
        return JsonResponse({'data': data})


class AppealsView(ListView):
    """
    Отображает список заявлений
    """
    model = Appeal
    template_name = 'core/appeals.html'

    def get_filters(self):
        return core.filters.AppealFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['average'] = Appeal.objects.aggregate(Avg('emergency_services'))['emergency_services__avg']
        context['filter'] = AppealFilter(self.request.GET)

        return context


class AppealDetailView(DetailView):
    """
    Отображает данные о заявлении
    """
    model = Appeal
    template_name = 'core/appeal_detail.html'


class ApplicantsView(ListView):
    """
    Отображает список заявителей
    """
    model = Applicant
    template_name = 'core/applicants.html'

    def get_filters(self):
        return core.filters.ApplicantFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ApplicantFilter(self.request.GET)

        return context


class ApplicantDetailView(DetailView):
    """
    Отображает данные о заявителе
    """
    model = Applicant
    template_name = 'core/applicant_detail.html'


class ServicesView(ListView):
    """
    Отображает список экстренных служб
    """
    model = EmergencyService
    template_name = 'core/services.html'


class ServiceDetailView(DetailView):
    """
    Отображает данные об экстренной службе
    """
    model = EmergencyService
    template_name = 'core/service_detail.html'


class Index(TemplateView):
    """
    Главная страница
    """
    template_name = 'core/index.html'


class AppealUpdateView(UpdateView):
    """
    Страница изменения заявления
    """
    model = Appeal
    template_name = 'core/update.html'
    form_class = AppealForm

    def get_success_url(self):
        return reverse('core:appeals')


class ApplicantUpdateView(UpdateView):
    """
    Страница изменения заявителя
    """
    model = Applicant
    template_name = 'core/update.html'
    form_class = ApplicantForm

    def get_success_url(self):
        return reverse('core:applicants')


class ServiceUpdateView(UpdateView):
    """
    Страница изменения службы
    """
    model = EmergencyService
    template_name = 'core/update.html'
    form_class = EmergencyServiceForm

    def get_success_url(self):
        return reverse('core:services')


class ServiceCreateView(CreateView):
    """
    Страница создания службы
    """
    model = EmergencyService
    template_name = 'core/create.html'
    form_class = EmergencyServiceForm

    def get_success_url(self):
        return reverse('core:services')


class ApplicantCreateView(CreateView):
    """
    Страница создания заявителя
    """
    model = Applicant
    template_name = 'core/create.html'
    form_class = ApplicantForm

    def get_success_url(self):
        return reverse('core:applicants')


class AppealCreateView(CreateView):
    """
    Страница создания заявленяи
    """
    model = Appeal
    template_name = 'core/create.html'
    form_class = AppealForm

    def get_success_url(self):
        return reverse('core:appeals')
