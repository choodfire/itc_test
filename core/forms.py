from django import forms
from .models import *
import datetime


class ApplicantForm(forms.ModelForm):
    birthday = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Выберите год", "Месяц", "День"),
    ),)

    def clean(self, *args, **kwargs):
        full_name = self.cleaned_data.get("full_name")
        birthday = self.cleaned_data.get("birthday")
        phone = self.cleaned_data.get("phone")
        health_status = self.cleaned_data.get("health_status")
        gender = self.cleaned_data.get("gender")

        if birthday.year > datetime.date.today().year:
            raise forms.ValidationError("Этот год еще не наступил")

        if len(str(phone)) > 11:
            raise forms.ValidationError("Длина телефона не больше 11 символов")

        return super(ApplicantForm, self).clean(*args, **kwargs)

    class Meta:
        model = Applicant
        fields = ['full_name', 'birthday', 'phone', 'health_status', 'gender', 'image']
        widgets = {
            "health_status": forms.Textarea(),
        }


class AppealForm(forms.ModelForm):
    emergency_services = forms.ModelMultipleChoiceField(
        queryset=EmergencyService.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True)

    class Meta:
        model = Appeal
        fields = ['status', 'victims_number', 'do_not_call', 'emergency_services', 'applicant']


class EmergencyServiceForm(forms.ModelForm):
    service_code = forms.CharField(help_text='Код экстренной службы')

    class Meta:
        model = EmergencyService
        fields = ["title", 'phone', 'service_code']
