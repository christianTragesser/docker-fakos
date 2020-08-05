from prometheus_client import start_http_server, Gauge, Histogram
import time
import os
import ping

gService = Gauge('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
gHost = Gauge('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])
gValidCertDays = Gauge('valid_cert_days_remaining', 'valid certificate days remaining(days)', ['service', 'namespace'])
hService = Histogram('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
hHost = Histogram('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])

interval = int(os.environ['INTERVAL']) if 'INTERVAL' in os.environ else 10


def record_metrics():
    stats = ping.measure_requests()
    for service in stats:
        hService.labels(service['name'], service['namespace']).observe(service['service_latency'])
        hHost.labels(service['name'], service['namespace']).observe(service['host_latency'])
        gService.labels(service['name'], service['namespace']).set(service['service_latency'])
        gHost.labels(service['name'], service['namespace']).set(service['host_latency'])
        gValidCertDays.labels(service['name'], service['namespace']).set(service['validCertDaysRemaining'])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Start measuring ingress/service latencies
    while True:
        try:
            record_metrics()
            time.sleep(interval)
        except Exception as e:
            print(e)
