from django.contrib import admin
from core.models import Appeal, Applicant, EmergencyService


class AppealAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'date')
    sortable_by = ('date', )
    empty_value_display = '-empty-'
    list_filter = ('date', )
    search_fields = ('status',)
    search_help_text = 'Поиск по статусу'


admin.site.register(Appeal, AppealAdmin)


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'health_status', 'get_appeals')
    list_editable = ('phone', )
    list_filter = ('phone', )
    search_fields = ('health_status',)
    search_help_text = 'Поиск по состоянию здоровья'
    readonly_fields = ('full_name',)
    empty_value_display = '-empty-'

    def get_author(self, obj):
        return "skibididondondon"

    def get_appeals(self, obj):
        return "Проишествия - " + ", ".join([str(apl) for apl in obj.applicants.all()])


admin.site.register(Applicant, ApplicantAdmin)


@admin.register(EmergencyService)
class EmergencyServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'phone', 'service_code')
    list_filter = ('service_code', )
    search_fields = ('phone',)
    search_help_text = 'Поиск по телефону'
    empty_value_display = '-empty-'
