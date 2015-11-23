from django.contrib import admin

from models import SolarPanel


class SolarPanelAdmin(admin.ModelAdmin):
    exclude = ["square_feet_access"]



admin.site.register(SolarPanel, SolarPanelAdmin)
