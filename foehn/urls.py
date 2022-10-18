from django.urls import path

from . import views

app_name = "foehn"

urlpatterns = [
    path(
        "graphes/powercurve/<uuid:pk>.json",
        views.PowerCurveChart.as_view(),
        name="graph_powercurve_data",
    ),
    path(
        "graphes/power_vs_windspeed/<uuid:pk>.json",
        views.PowerVsWindSpeedChart.as_view(),
        name="graph_powervswindspeed_data",
    ),
    path(
        "graphes/wind_distribution/<uuid:pk>.json",
        views.WindDistributionChart.as_view(),
        name="graph_winddistribution_data",
    ),
    path(
        "graphes/wind_resource/<uuid:pk>.json",
        views.WindResourceChart.as_view(),
        name="graph_windresource_data",
    ),
    path(
        "graphes/montlthly_production/<uuid:pk>.json",
        views.MonthlyProductionChart.as_view(),
        name="graph_monthlyproduction_data",
    ),
    path("", views.index, name="index"),
]
