from prometheus_client import start_http_server, Gauge, Histogram
import time
import ping

gService = Gauge('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
gHost = Gauge('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])
hService = Histogram('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
hHost = Histogram('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])

def recordMetrics():
    stats = ping.measureRequests()
    for service in stats:
        hService.labels(service['name'], service['namespace']).observe(service['service_latency'])
        hHost.labels(service['name'], service['namespace']).observe(service['host_latency'])
        gService.labels(service['name'], service['namespace']).set(service['service_latency'])
        gHost.labels(service['name'], service['namespace']).set(service['host_latency'])

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Start measuring ingress/service latencies
    while True:
        try:
            recordMetrics()
            time.sleep(10)
        except ValueError as e:
            print e