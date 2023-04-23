from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('first/', views.FirstView.as_view(), name='first'),
    path('second/<int:pk>/', views.SecondView.as_view(), name='second'),
    path('third/', views.ThirdView.as_view(), name='third'),
    path('fourth/', views.FourthView.as_view(), name='fourth'),
    path('fifth/', views.FifthView.as_view(), name='fifth'),
    path('sixth/', views.SixthView.as_view(), name='sixth'),

    path('appeals/', views.AppealsView.as_view(), name='appeals'),
    path('appeals/<int:pk>/', views.AppealDetailView.as_view(), name='appeal_detail'),

    path('applicants/', views.ApplicantsView.as_view(), name='applicants'),
    path('applicants/<int:pk>/', views.ApplicantDetailView.as_view(), name='applicant_detail'),

    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),

    path('', views.Index.as_view(), name='index'),
]
