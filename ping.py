import os
import sys
import time
import requests
import urllib3


#service_name = os.environ['SERVICE_NAME']
#python_service_name = service_name.replace('-', '_') #convert hyphens to underscore to be python friendly
#namespace = os.environ['NAMESPACE']
#port = os.environ['PORT']
#ingress_host = os.environ['URL']
#user = os.environ['USER']
#password = os.environ['PASS']

def constructURL():
    endpoints = [ { 'service': 'none', 'host': 'none'} ]
    return endpoints