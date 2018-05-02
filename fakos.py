#!/usr/local/bin/python

from kubernetes import client, config
import json
import time

# uncomment below for local development providing kubeconfig path
# config.load_kube_config('./config')

# or use the paths below to utilize certs provided by service account
tokenFile = "/var/run/secrets/kubernetes.io/serviceaccount/token"
caFile = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

with open (tokenFile, "r") as apiToken:
    token = apiToken.read()

config = client.Configuration()
config.host = "https://kubernetes.default.svc.cluster.local"
config.api_key = {"authorization": "Bearer " + token}
config.ssl_ca_cert = caFile

client.Configuration.set_default(config)

v1beta1 = client.ExtensionsV1beta1Api()

while True: 
    response = json.load(v1beta1.list_ingress_for_all_namespaces(_preload_content=False))
    for item in response['items']:
        namespace = item['metadata']['namespace']
        for rule in item['spec']['rules']:
            host = rule['host']
            for path in rule['http']['paths']:
                service_name = path['backend']['serviceName']
        print "FQDN: %s, service: %s.%s.cluster.local" % (host, service_name, namespace)
        print "**********************"
    time.sleep(3)