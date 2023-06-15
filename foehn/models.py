from typing import List
from uuid import uuid4 as UUID4

from django.db import models
from django.db.models import Sum


class PowerCurve(models.Model):
    MIN_SPEED = 0
    MAX_SPEED = 25
    RANGE_SPEED = range(0, 25 + 1)

    uuid = models.UUIDField(default=UUID4, primary_key=True)

    def __getitem__(self, wind_speed: int) -> float:
        return getattr(self, f"wind_speed_{wind_speed}ms")

    def __setitem__(self, wind_speed: int, power: float) -> None:
        setattr(self, f"wind_speed_{wind_speed}ms", power)

    def as_list(self) -> List[float]:
        return [self[wind_speed] for wind_speed in range(self.MAX_SPEED + 1)]

    def from_list(self, powers: List[float]) -> None:
        assert len(powers) == self.MAX_SPEED + 1

        for wind_speed, power in enumerate(powers):
            self[wind_speed] = power

# Programmatically create the wind speed bucket attributes
for speed in PowerCurve.RANGE_SPEED:
    PowerCurve.add_to_class(f"wind_speed_{speed}ms", models.FloatField(default=0))

##############################################################################
# Knowledges
class Manufacturer(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


class TurbineModel(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name="models"
    )
    reference_power_curve = models.OneToOneField(
        PowerCurve,
        on_delete=models.CASCADE,
        related_name="turbine_model",
        default=PowerCurve,
    )

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


##############################################################################
# Assets management


class Organization(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


class Site(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="sites"
    )

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


class Turbine(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="turbines"
    )
    model = models.ForeignKey(
        TurbineModel, on_delete=models.CASCADE, related_name="turbines"
    )
    power_curve = models.OneToOneField(
        PowerCurve,
        on_delete=models.CASCADE,
        related_name="turbine",
        default=PowerCurve,
    )

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )

    def total_production(self) -> float:
        return (
            self.records.filter(active_power__gt=0).aggregate(
                total_production=Sum("active_power")
            )["total_production"]
            // 6
            // 1000000
        )


##############################################################################
# Scada
class ScadaFileFormat(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    name = models.CharField(max_length=256)
    turbine_name_column = models.CharField(max_length=256)
    timestamp_column = models.CharField(max_length=256)
    wind_speed_column = models.CharField(max_length=256)
    wind_direction_column = models.CharField(max_length=256)
    air_temperature_column = models.CharField(max_length=256)
    nacelle_direction_column = models.CharField(max_length=256)
    active_power_column = models.CharField(max_length=256)
    pitch_angle_column = models.CharField(max_length=256)

    def __str__(self):
        return self.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


class ScadaFile(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    site = models.ForeignKey(
        Site, on_delete=models.CASCADE, related_name="scada_files"
    )
    upload = models.FileField(upload_to="uploads/scada/%Y/%m/%d/")
    file_format = models.ForeignKey(
        ScadaFileFormat, on_delete=models.CASCADE, related_name="files"
    )

    def __str__(self):
        return self.upload.name or "<Unamed {}(uuid={})>".format(
            self.__class__.name, self.uuid
        )


class ScadaRecord(models.Model):
    uuid = models.UUIDField(default=UUID4, primary_key=True)
    turbine = models.ForeignKey(
        Turbine, on_delete=models.CASCADE, related_name="records"
    )
    scada_file = models.ForeignKey(
        ScadaFile, on_delete=models.CASCADE, related_name="records"
    )
    timestamp = models.DateTimeField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()
    air_temperature = models.FloatField()
    nacelle_direction = models.FloatField()
    active_power = models.FloatField()
    pitch_angle = models.FloatField()
