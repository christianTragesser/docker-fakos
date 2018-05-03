import os
import sys
import time
import requests
import urllib3
import ingress


def constructURL():
    global ingress
    endpoints = []
    ingressData = ingress.getIngress()
    for ingress in ingressData:
        urls = {}
        urls['host'] = 'https://'+ingress['host']
        urls['service'] = 'http://'+ingress['serviceName']+'.'+ingress['namespace']+'.svc.cluster.local'
        endpoints.append(urls)
    return endpoints