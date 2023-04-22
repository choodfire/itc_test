from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('first/', views.FirstView.as_view(), name='first'),
    path('second/<int:pk>/', views.SecondView.as_view(), name='second'),
    path('third/', views.ThirdView.as_view(), name='first'),
    path('fourth/', views.FourthView.as_view(), name='fourth'),
    path('fifth/', views.FifthView.as_view(), name='fifth'),
    path('sixth/', views.SixthView.as_view(), name='sixth'),
]
