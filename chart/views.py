from typing import Any, Dict, List, Optional

from django.http.response import JsonResponse
from django.views import View


class ChartView(View):
    def __init__(
        self,
        kind: str,
        labels: Optional[str] = None,
        datasets: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.kind = kind
        self.labels = labels
        self.datasets = datasets
        self.options = options

    def prepare_data(self):
        ...

    def get_labels(self) -> Optional[List[str]]:
        return self.labels

    def get_datasets(self) -> List[Dict[str, Any]]:
        return self.datasets or []

    def get_options(self) -> Dict[str, Any]:
        return self.options or {}

    def get(self, request, *args, **kwargs):
        self.prepare_data()

        data = {}
        labels = self.get_labels()
        if labels is not None:
            data["labels"] = labels
        data["datasets"] = self.get_datasets()

        config = {}
        config["type"] = self.kind
        config["data"] = data
        config["options"] = self.get_options()

        return JsonResponse(config)


class BarChartView(ChartView):
    def __init__(
        self,
        labels: Optional[str] = None,
        datasets: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            "bar", labels=labels, datasets=datasets, options=options
        )


class LineChartView(ChartView):
    def __init__(
        self,
        labels: Optional[str] = None,
        datasets: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            "line", labels=labels, datasets=datasets, options=options
        )


class ScatterChartView(ChartView):
    def __init__(
        self,
        datasets: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__("scatter", datasets=datasets, options=options)

    def get_labels(self) -> Optional[List[str]]:
        return None


class PolarAreaChartView(ChartView):
    def __init__(
        self,
        labels: Optional[str] = None,
        datasets: Optional[List[Dict[str, Any]]] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            "polarArea", labels=labels, datasets=datasets, options=options
        )
