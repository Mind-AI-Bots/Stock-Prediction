from prometheus_client import Counter
import os
from typing import Callable
import numpy as np
from prometheus_client import Histogram
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

NAMESPACE = os.environ.get("METRICS_NAMESPACE", "fastapi")
SUBSYSTEM = os.environ.get("METRICS_SUBSYSTEM", "model")

instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)


# ----- custom metrics -----
def stock_prediction_models(
    metric_name: str = "stock_prediction_models",
    metric_doc: str = "Output value of stock_prediction_models",
    metric_namespace: str = "",
    metric_subsystem: str = "",
    buckets=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, float("inf")),
) -> Callable[[Info], None]:
    METRIC = Histogram(
        metric_name,
        metric_doc,
        buckets=buckets,
        namespace=metric_namespace,
        subsystem=metric_subsystem,
    )
    METRIC.labels("Linear Regression Model")
    METRIC.labels("LSTM Model")
    METRIC.labels("k-Nearest Neighbour Model")

    def instrumentation(info: Info) -> None:
        if info.modified_handler == "/listmodels":
            model_prediction = info.response.headers.get("X-model-prediction")
            model_type=info.response.headers.get("X-model-type")
            if model_prediction:
                METRIC.labels(model_type).observe(float(model_prediction))
    return instrumentation


# ----- add metrics -----
instrumentator.add(
    metrics.request_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.response_size(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.latency(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)
instrumentator.add(
    metrics.requests(
        should_include_handler=True,
        should_include_method=True,
        should_include_status=True,
        metric_namespace=NAMESPACE,
        metric_subsystem=SUBSYSTEM,
    )
)

buckets = (*np.arange(0, 10.5, 0.5).tolist(), float("inf"))
instrumentator.add(
    stock_prediction_models(metric_namespace=NAMESPACE, metric_subsystem=SUBSYSTEM, buckets=buckets)
)
