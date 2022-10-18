from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Avg

from ...models import ScadaRecord, Turbine


def recompute_power_curves():
    for turbine in Turbine.objects.all():
        print("turbine", turbine.name)
        recompute_power_curve_for_turbine(turbine)


def recompute_power_curve_for_turbine(turbine: Turbine):
    power_curve = turbine.power_curve
    for wind_speed in range(26):
        power_curve[wind_speed] = (
            turbine.records.filter(
                wind_speed__range=(wind_speed, wind_speed + 1),
                active_power__gt=0,
            ).aggregate(power=Avg("active_power"))["power"]
            or 0
        )

    power_curve.save()


class Command(BaseCommand):
    help = "Recompute the power curves"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("scada_file_uuids", nargs="+", type=int)

    def handle(self, *args, **options):
        recompute_power_curves()
