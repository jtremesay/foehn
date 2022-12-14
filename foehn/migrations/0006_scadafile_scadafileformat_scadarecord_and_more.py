# Generated by Django 4.1 on 2022-09-01 17:08

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("foehn", "0005_turbine"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScadaFile",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "upload",
                    models.FileField(upload_to="uploads/scada/%Y/%m/%d/"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScadaFileFormat",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("turbine_name_column", models.CharField(max_length=256)),
                ("timestamp_column", models.CharField(max_length=256)),
                ("wind_speed_column", models.CharField(max_length=256)),
                ("wind_direction_column", models.CharField(max_length=256)),
                ("air_temperature_column", models.CharField(max_length=256)),
                ("nacelle_direction_column", models.CharField(max_length=256)),
                ("active_power_column", models.CharField(max_length=256)),
                ("pitch_angle_column", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="ScadaRecord",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("timestamp", models.DateTimeField()),
                ("wind_speed", models.FloatField()),
                ("wind_direction", models.FloatField()),
                ("air_temperature", models.FloatField()),
                ("nacelle_direction", models.FloatField()),
                ("active_power", models.FloatField()),
                ("pitch_angle", models.FloatField()),
                (
                    "scada_file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="foehn.scadafile",
                    ),
                ),
                (
                    "turbine",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="records",
                        to="foehn.turbine",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="scadafile",
            name="file_format",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="foehn.scadafileformat",
            ),
        ),
        migrations.AddField(
            model_name="scadafile",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scada_files",
                to="foehn.site",
            ),
        ),
    ]
