import requests
import ingress
import sslCheck
import logs
from multiprocessing import Pool, cpu_count

log = logs.logger('ping')

def constructURLs():
    global ingress
    endpoints = []
    ingressData = ingress.getIngressList()
    for service in ingressData:
        servicePort = str(service['servicePort'])
        urls = {}
        urls['name'] = service['name']
        urls['host'] = service['host']
        urls['service'] = service['serviceName']+'.'+service['namespace']+'.svc.cluster.local:'+servicePort
        urls['namespace'] = service['namespace']
        endpoints.append(urls)
    return endpoints

def measureRequests():
    urlObjects = constructURLs()
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
    latencies = []
    for path in servicePaths:
        latencies.append(getRequestDuration(path))

    validDays = sslCheck.certDaysRemaining(urlObject['host'])

    measurement = {}
    measurement['service_latency'] = latencies[0]
    measurement['host_latency'] = latencies[1]
    measurement['name'] = urlObject['name']
    measurement['namespace'] = urlObject['namespace']
    measurement['validCertDaysRemaining'] = validDays
    
    log.info(measurement)
    return measurement