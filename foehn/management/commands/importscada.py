import math

import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from ...models import ScadaFile, ScadaRecord


def import_scada_files():
    for scada_file in ScadaFile.objects.all():
        import_scada_file(scada_file)


def import_scada_file(scada_file: ScadaFile):
    print("importing", scada_file.upload)
    # Generate the list of columns to get
    file_format = scada_file.file_format

    # Read the scada file
    columns_names = [
        file_format.turbine_name_column,
        file_format.timestamp_column,
        file_format.wind_speed_column,
        file_format.wind_direction_column,
        file_format.air_temperature_column,
        file_format.nacelle_direction_column,
        file_format.active_power_column,
        file_format.pitch_angle_column,
    ]
    scada_data = pd.read_csv(
        scada_file.upload,
        usecols=columns_names,
        sep=";",
    )

    # Get the turbines in the scada file
    turbines_names = scada_data[file_format.turbine_name_column].unique()
    turbines = scada_file.site.turbines.filter(name__in=turbines_names)
    turbines_cache = {t.name: t for t in turbines}
    print("find turbines", ", ".join(turbines_names))

    # Load the records
    records = []
    for idx, row in scada_data.iterrows():
        turbine_name = row[file_format.turbine_name_column]
        turbine = turbines_cache[turbine_name]
        scada_record = ScadaRecord(
            turbine=turbine,
            scada_file=scada_file,
            timestamp=row[file_format.timestamp_column],
            wind_speed=row[file_format.wind_speed_column]
            if not math.isnan(row[file_format.wind_speed_column])
            else 0,
            wind_direction=row[file_format.wind_direction_column]
            if not math.isnan(row[file_format.wind_direction_column])
            else 0,
            air_temperature=row[file_format.air_temperature_column]
            if not math.isnan(row[file_format.air_temperature_column])
            else 0,
            nacelle_direction=row[file_format.nacelle_direction_column]
            if not math.isnan(row[file_format.nacelle_direction_column])
            else 0,
            active_power=row[file_format.active_power_column]
            if not math.isnan(row[file_format.active_power_column])
            else 0,
            pitch_angle=row[file_format.pitch_angle_column]
            if not math.isnan(row[file_format.pitch_angle_column])
            else 0,
        )
        records.append(scada_record)

    with transaction.atomic():
        print("deleting old records")
        ScadaRecord.objects.filter(scada_file=scada_file).delete()
        print("importing", len(records), "records")
        ScadaRecord.objects.bulk_create(records)
        print("validating transaction")


class Command(BaseCommand):
    help = "Import the unimported scada files"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("scada_file_uuids", nargs="+", type=int)

    def handle(self, *args, **options):
        import_scada_files()
