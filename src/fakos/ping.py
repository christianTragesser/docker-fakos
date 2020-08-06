from multiprocessing import Pool
from fakos import ingress, ssl_check, fakos_log
import requests

log = fakos_log.logger('ping')


def construct_service_url(data):
    data['service'] = data['serviceName'] + '.' + data['namespace'] + '.svc.cluster.local:' + str(data['servicePort'])
    return data


def construct_endpoints():
    ingressData = ingress.get_ingress_list()
    endpoints = (construct_service_url(service) for service in ingressData)
    return tuple(endpoints)


def get_request_duration(url):
    try:
        r = requests.get(url)
        return r.elapsed.total_seconds()
    except Exception as e:
        log.error(e)
        return -1


def construct_results(url_object):
    servicePaths = ['http://' + url_object['service'], 'https://' + url_object['host']]
    latencies = [get_request_duration(path) for path in servicePaths]
    validDays = ssl_check.cert_days_remaining(url_object['host'])

    measurement = {}
    measurement['service_latency'] = latencies[0]
    measurement['host_latency'] = latencies[1]
    measurement['name'] = url_object['name']
    measurement['namespace'] = url_object['namespace']
    measurement['cert_expire_days'] = validDays

    log.info(measurement)
    return measurement


def measure_requests():
    url_endpoints = construct_endpoints()
    # parallel latency requests
    pool = Pool()
    measurements = tuple(pool.map(construct_results, url_endpoints))
    return measurements
