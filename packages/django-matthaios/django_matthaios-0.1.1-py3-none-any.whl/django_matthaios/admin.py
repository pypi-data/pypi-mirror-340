from django.contrib import admin
from django.conf import settings
from .models import Party, CounterParty, Address, PartySet

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    fields = ('adr1', 'type', 'postal_code', 'city', 'is_default')

class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'party_number', 'id')
    search_fields = ('name', 'party_number')
    inlines = [AddressInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Address) and not instance.counterparty:
                instance.party = form.instance
                instance.save()
        formset.save_m2m()

class CounterPartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    inlines = [AddressInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Address) and not instance.party:
                instance.counterparty = form.instance
                instance.save()
        formset.save_m2m()

class AddressAdmin(admin.ModelAdmin):
    list_display = ('adr1', 'type', 'postal_code', 'city', 'party', 'counterparty', 'is_default')
    list_filter = ('type', 'is_default')
    search_fields = ('adr1', 'postal_code', 'city')
    raw_id_fields = ('party', 'counterparty')

class PartySetAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('parties',)

# Conditional registration based on a setting
REGISTER_ADMIN = getattr(settings, 'MATTHAIOS_REGISTER_ADMIN', True)

if REGISTER_ADMIN:
    admin.site.register(Party, PartyAdmin)
    admin.site.register(CounterParty, CounterPartyAdmin)
    admin.site.register(PartySet, PartySetAdmin)