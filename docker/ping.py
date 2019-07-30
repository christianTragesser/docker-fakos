import requests
import ingress
import sslCheck
import logs
from multiprocessing import Pool, cpu_count

log = logs.logger('ping')

def construct_service_url(data):
    data['service'] = data['serviceName']+'.'+data['namespace']+'.svc.cluster.local:'+str(data['servicePort'])
    return data

def construct_endpoints():
    ingressData = ingress.get_ingress_list()
    endpoints = [ construct_service_url(service) for service in ingressData ]
    return endpoints

def measureRequests():
    urlObjects = construct_endpoints()
    # split endpoint latency requests across number of available host processors
    processes = cpu_count()
    pool = Pool(processes)
    measurements = list(pool.map(constructResults, urlObjects))
    return measurements

def getRequestDuration(url):
    try:
        r = requests.get(url)
        return r.elapsed.total_seconds()
    except Exception as e:
        log.error(e)
        return -1

def constructResults(urlObject):
    servicePaths = [ 'http://'+urlObject['service'], 'https://'+urlObject['host'] ]
    latencies = [ getRequestDuration(path) for path in servicePaths ]
    validDays = sslCheck.certDaysRemaining(urlObject['host'])

    measurement = {}
    measurement['service_latency'] = latencies[0]
    measurement['host_latency'] = latencies[1]
    measurement['name'] = urlObject['name']
    measurement['namespace'] = urlObject['namespace']
    measurement['validCertDaysRemaining'] = validDays
    
    log.info(measurement)
    return measurement