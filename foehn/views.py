import math
from typing import Any, Dict, List, Optional

from django.db.models import Sum
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin

from chart.views import (
    BarChartView,
    LineChartView,
    PolarAreaChartView,
    ScatterChartView,
)

from .models import Organization, PowerCurve, Site, Turbine, TurbineModel


class TurbineChartMixin(SingleObjectMixin):
    model = Turbine

    def get(self, request, *args, **kwargs):
        self.turbine = self.get_object()
        return super().get(request, *args, **kwargs)


class PowerCurveChart(TurbineChartMixin, LineChartView):
    def get_labels(self) -> Optional[List[str]]:
        return [f"{ws} m.s⁻¹" for ws in range(PowerCurve.MAX_SPEED + 1)]

    def get_datasets(self) -> List[Dict[str, Any]]:
        return [
            {
                "label": self.turbine.name,
                "data": self.turbine.power_curve.as_list(),
                "backgroundColor": "rgb(0, 127, 255)",
            },
            {
                "label": "ref. manuf.",
                "data": self.turbine.model.reference_power_curve.as_list(),
                "backgroundColor": "rgb(255, 127, 0)",
            },
        ]


class PowerVsWindSpeedChart(TurbineChartMixin, ScatterChartView):
    def get_datasets(self) -> List[Dict[str, Any]]:
        return [
            {
                "label": "Power (kW) vs wind speed (m.s⁻¹)",
                "data": [
                    {"x": r["wind_speed"], "y": r["active_power"]}
                    for r in self.turbine.records.filter(active_power__gt=0)
                    .order_by("?")
                    .values("wind_speed", "active_power")[:1000]
                ],
                "backgroundColor": "rgb(0, 127, 255)",
            },
        ]


class WindDistributionChart(TurbineChartMixin, PolarAreaChartView):
    SECTOR_SIZE = 30

    def get_labels(self) -> Optional[List[str]]:
        return [f"[{a}°, {a + 15}°[" for a in range(0, 360, self.SECTOR_SIZE)]

    def get_datasets(self) -> List[Dict[str, Any]]:
        records_count = self.turbine.records.count()
        return [
            {
                "label": "Wind distribution",
                "data": [
                    self.turbine.records.filter(
                        wind_direction__range=[a, a + self.SECTOR_SIZE]
                    ).count()
                    / records_count
                    for a in range(0, 360, self.SECTOR_SIZE)
                ],
                "backgroundColor": [
                    f"rgb({((math.cos(a * math.pi / 180) + 1) / 2) * 255}, 127, {((math.sin(a * math.pi / 180) + 1) / 2) * 255})"
                    for a in range(0, 360, self.SECTOR_SIZE)
                ],
            },
        ]


class WindResourceChart(TurbineChartMixin, BarChartView):
    def get_labels(self) -> Optional[List[str]]:
        return [f"{ws} m.s⁻¹" for ws in range(PowerCurve.MAX_SPEED + 1)]

    def get_datasets(self) -> List[Dict[str, Any]]:
        records_count = self.turbine.records.count()

        return [
            {
                "label": "wind resource",
                "data": [
                    self.turbine.records.filter(
                        wind_speed__range=(ws, ws + 1)
                    ).count()
                    / records_count
                    for ws in range(
                        PowerCurve.MIN_SPEED, PowerCurve.MAX_SPEED + 1
                    )
                ],
                "backgroundColor": "rgb(0, 127, 255)",
            },
        ]


class MonthlyProductionChart(TurbineChartMixin, BarChartView):
    def prepare_data(self):
        self.labels = []
        data = []
        current_month = (
            self.turbine.records.order_by("timestamp")
            .first()
            .timestamp.replace(day=1, hour=0, minute=0, second=0)
        )

        last_month = (
            self.turbine.records.order_by("-timestamp")
            .first()
            .timestamp.replace(day=1, hour=0, minute=0, second=0)
        )
        if last_month.month == 12:
            last_month = last_month.replace(year=last_month.year + 1, month=1)
        else:
            last_month = last_month.replace(month=last_month.month + 1)

        while current_month < last_month:
            if current_month.month == 12:
                next_month = current_month.replace(
                    year=current_month.year + 1, month=1
                )
            else:
                next_month = current_month.replace(
                    month=current_month.month + 1
                )

            self.labels.append(f"{current_month.year}-{current_month.month}")
            production = self.turbine.records.filter(
                active_power__gt=0,
                timestamp__range=(current_month, next_month),
            ).aggregate(total_production=Sum("active_power"))[
                "total_production"
            ]
            if production is None:
                production = 0
            else:
                production = production / 6 / 1000

            data.append(production)

            current_month = next_month

        self.datasets = [
            {
                "label": "monthly production (MWh)",
                "data": data,
                "backgroundColor": "rgb(0, 127, 255)",
            },
        ]


def index(request: HttpRequest) -> HttpResponse:
    ctx = {}
    ctx["turbines"] = Turbine.objects.order_by("name")

    return render(request, "foehn/index.html", ctx)
