from prometheus_client import start_http_server, Gauge, Histogram
from pythonjsonlogger import jsonlogger
import logging
import time
import sys
import ping

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

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
        log.info(service)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Start measuring ingress/service latencies
    while True:
        try:
            recordMetrics()
            time.sleep(10)
        except Exception, e:
            log.error(e)