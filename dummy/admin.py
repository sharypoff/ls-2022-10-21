from django.contrib import admin
from .models import SimpleLamp, Chandelier, \
    Airport, Ticket, PassangerInfo

admin.site.empty_value_display = '(Нет)'


class SimpleLampInline(admin.TabularInline):
    model = SimpleLamp


# admin.site.register(SimpleLamp)
@admin.register(SimpleLamp)
class AdminSimpleLamp(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('address', 'lamp_type'), 'power', 'chandelier'),
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('is_switched_on', 'colorful_temperature'),
        }),
    )
    list_display = ('__str__', 'address', 'lamp_type', 'power')
    search_fields = ['address']


@admin.register(Chandelier)
class AdminChandelier(admin.ModelAdmin):
    inlines = [
        SimpleLampInline
    ]


admin.site.register(Airport)
admin.site.register(Ticket)
admin.site.register(PassangerInfo)
