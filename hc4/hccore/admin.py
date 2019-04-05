from cities_light.admin import CountryAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from hvad.admin import TranslatableAdmin
from . import models


class HCCountryAdmin(CountryAdmin):
    autocomplete_fields = ['capital']


class AddressAdmin(TranslatableAdmin):
    autocomplete_fields = ['city']


class MemberContactInline(admin.TabularInline):
    model = models.MemberContact
    fields = ['contact_method', 'contact_detail', 'preferred', 'share_by_default']
    extra = 0
    min_num = 0


class MemberLanguageInline(admin.TabularInline):
    model = models.MemberLanguage
    fields = ['language', 'level', 'primary']
    extra = 0
    min_num = 0


class MemberTravelInline(admin.TabularInline):
    model = models.MemberTravel
    fields = ['city', 'plan', 'visit_date_from', 'visit_date_to', 'hc_experience']
    autocomplete_fields = ['city']
    extra = 0
    min_num = 0


class MemberInterestInline(admin.TabularInline):
    model = models.MemberInterest
    fields = ['interest']
    extra = 0
    min_num = 0


class MemberAdmin(admin.ModelAdmin):
    inlines = [
        MemberContactInline, 
        MemberTravelInline,
        MemberLanguageInline,
        MemberInterestInline,
    ]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    autocomplete_fields = ['user']


class MemberTravelAdmin(TranslatableAdmin):
    autocomplete_fields = ['member', 'city']


admin.site.site_header = _("Hospitality Club Admin")
if admin.site.is_registered(models.Country):
    admin.site.unregister(models.Country)
admin.site.register(models.Country, HCCountryAdmin)
admin.site.register(models.Address, AddressAdmin)
admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Language)
admin.site.register(models.Interest)
admin.site.register(models.MemberTravel, MemberTravelAdmin)
admin.site.register(models.MemberLoginHistory)
admin.site.register(models.MemberRelation)
admin.site.register(models.Message)
