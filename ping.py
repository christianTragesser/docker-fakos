import requests
import ingress

def constructURLs():
    global ingress
    endpoints = []
    ingressData = ingress.getIngressList()
    for service in ingressData:
        urls = {}
        urls['name'] = service['name']
        urls['host'] = 'https://'+service['host']
        urls['service'] = 'http://'+service['serviceName']+'.'+service['namespace']+'.svc.cluster.local'
        endpoints.append(urls)
    return endpoints

def measureRequests():
    stats = []
    urlObjects = constructURLs()
    for service in urlObjects:
        measurements = {}
        measurements['name'] = service['name']
        measurements['service_latency'] = getRequestDuration(service['service'])
        measurements['host_latency'] = getRequestDuration(service['host'])
        stats.append(measurements)
    return stats

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
        print e
        return 0