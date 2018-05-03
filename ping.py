import os
import sys
import time
import requests
import urllib3
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
    return True