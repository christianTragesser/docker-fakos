import os
from prometheus_client import start_http_server, Gauge, Histogram
from time import sleep
from fakos import ping

g_service = Gauge('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
g_host = Gauge('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])
g_valid_cert_days = Gauge('valid_cert_days_remaining', 'valid certificate days remaining(days)', ['service', 'namespace'])
h_service = Histogram('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
h_host = Histogram('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])

interval = int(os.environ['INTERVAL']) if 'INTERVAL' in os.environ else 30
interval *= 60


def record_metrics():
    stats = ping.measure_requests()
    for service in stats:
        h_service.labels(service['name'], service['namespace']).observe(service['service_latency'])
        h_host.labels(service['name'], service['namespace']).observe(service['host_latency'])
        g_service.labels(service['name'], service['namespace']).set(service['service_latency'])
        g_host.labels(service['name'], service['namespace']).set(service['host_latency'])
        g_valid_cert_days.labels(service['name'], service['namespace']).set(service['cert_expire_days'])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Start measuring ingress/service latencies
    while True:
        try:
            record_metrics()
            sleep(interval)
        except Exception as e:
            print(e)
