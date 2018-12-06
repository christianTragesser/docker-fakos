import requests
import ingress
import sslCheck
import logging
import sys
from pythonjsonlogger import jsonlogger
from multiprocessing import Pool, cpu_count

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
log.addHandler(logHandler)

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
        #request not able to reach service, return 0s response time
        #log.error(e)
        return 0

def constructResults(urlObject):
    servicePaths = [ 'http://'+urlObject['service'], 'https://'+urlObject['host'] ]
    latencies = []
    for path in servicePaths:
        latencies.append(getRequestDuration(path))

    print(latencies)
    try:
        print(urlObject['host'])
        validDays = sslCheck.certDaysRemaining(urlObject['host'])
    except Exception as e:
        print('Your cert check is failing because your passing the protocol with the FQDN')
        print(e)

    measurement = {}
    measurement['service_latency'] = latencies[0]
    measurement['host_latency'] = latencies[1]
    measurement['name'] = urlObject['name']
    measurement['namespace'] = urlObject['namespace']
    measurement['validCertDaysRemaining'] = validDays
    
    log.info(measurement)
    return measurement