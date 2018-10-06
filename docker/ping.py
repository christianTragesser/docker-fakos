import requests
import ingress
from multiprocessing import Pool
from multiprocessing import cpu_count

def constructURLs():
    global ingress
    endpoints = []
    ingressData = ingress.getIngressList()
    for service in ingressData:
        servicePort = str(service['servicePort'])
        urls = {}
        urls['name'] = service['name']
        urls['host'] = 'https://'+service['host']
        urls['service'] = 'http://'+service['serviceName']+'.'+service['namespace']+'.svc.cluster.local:'+servicePort
        urls['namespace'] = service['namespace']
        endpoints.append(urls)
    return endpoints

def measureRequests():
    urlObjects = constructURLs()
    # split endpoint latency requests across number of available host processors
    processes = cpu_count()
    pool = Pool(processes)
    return list(pool.map(constructResults, urlObjects))

def constructResults(urlObject):
    servicePaths = [ urlObject['service'], urlObject['host'] ]
    latencies = list(map(getRequestDuration, servicePaths))

    measurement = {}
    measurement['service_latency'] = latencies[0]
    measurement['host_latency'] = latencies[1]
    measurement['name'] = urlObject['name']
    measurement['namespace'] = urlObject['namespace']
    return measurement

def getRequestDuration(url):
    try:
        r = requests.get(url)
        #if request returns non success, return 0
        if r.status_code > 307:
            return 0
        else:
            return r.elapsed.total_seconds()
    except requests.exceptions.RequestException as e:
        #request not able to reach service, return 0s response time
        print(e)
        return 0