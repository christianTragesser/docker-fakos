from prometheus_client import start_http_server, Summary
import time
import ping

sService = Summary('service_latency_seconds', 'service latency(sec)', ['service', 'namespace'])
sHost = Summary('host_latency_seconds', 'host latency(sec)', ['service', 'namespace'])

def recordMetrics():
    stats = ping.measureRequests()
    for service in stats:
        sService.labels(service['name'], service['namespace']).observe(service['service_latency'])
        sHost.labels(service['name'], service['namespace']).observe(service['host_latency'])

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Start measuring ingress/service latencies
    while True:
        try:
            recordMetrics()
            time.sleep(5)
        except ValueError as e:
            print e