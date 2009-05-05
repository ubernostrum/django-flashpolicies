from django.contrib import admin

from flashpolicy.models import PermittedDomain
from flashpolicy.models import Policy


class PermittedDomainInline(admin.StackedInline):
    extra = 3
    model = PermittedDomain


class PolicyAdmin(admin.ModelAdmin):
    list_display = ('site', 'site_control', 'allow_all')
    inlines = [
        PermittedDomainInline,
        ]


admin.site.register(Policy, PolicyAdmin)
