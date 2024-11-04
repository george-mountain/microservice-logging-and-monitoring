from prometheus_client import Counter

# Prometheus counter for request metrics
request_counter = Counter(
    "requests_total", "Total number of requests", ["endpoint", "method", "status"]
)
