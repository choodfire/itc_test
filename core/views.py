from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.views.generic import TemplateView, DetailView
from .models import Appeal, Applicant
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


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
