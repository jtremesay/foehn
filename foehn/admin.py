from django.contrib import admin

from .models import (
    Manufacturer,
    Organization,
    PowerCurve,
    ScadaFile,
    ScadaFileFormat,
    ScadaRecord,
    Site,
    Turbine,
    TurbineModel,
)


@admin.register(PowerCurve)
class PowerCurveAdmin(admin.ModelAdmin):
    list_display = ("uuid", "turbine_model", "turbine")


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("uuid", "organization", "name")


@admin.register(Turbine)
class TurbineAdmin(admin.ModelAdmin):
    list_display = ("uuid", "organization", "site", "name", "model")

    @admin.display
    def organization(self, turbine):
        return turbine.site.organization


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")


@admin.register(TurbineModel)
class TurbineModelAdmin(admin.ModelAdmin):
    list_display = ("uuid", "manufacturer", "name", "reference_power_curve")


@admin.register(ScadaFileFormat)
class ScadaFileFormatAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name")


@admin.register(ScadaFile)
class ScadaFileAdmin(admin.ModelAdmin):
    list_display = ("uuid", "upload", "file_format")


@admin.register(ScadaRecord)
class ScadaRecordFileAdmin(admin.ModelAdmin):
    list_display = (
        "uuid",
        "turbine",
        "scada_file",
        "timestamp",
        "wind_speed",
        "wind_direction",
        "air_temperature",
        "nacelle_direction",
        "active_power",
        "pitch_angle",
    )
