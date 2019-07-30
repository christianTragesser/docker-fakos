from kubernetes import client, config
import json
import os
import logs

log = logs.logger('ingress')

def get_kube_credentials():
    tokenFile = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    caFile = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
    scriptDir = (os.path.dirname(os.path.realpath(__file__)))
    test_config = scriptDir+'/test/sample.config'

    if os.path.exists(tokenFile) and os.path.exists(caFile):
        with open (tokenFile, "r") as apiToken:
            token = apiToken.read()
        apiToken.close
        kube_config = client.Configuration()
        kube_config.host = "https://kubernetes.default.svc.cluster.local"
        kube_config.api_key = {"authorization": "Bearer " + token}
        kube_config.ssl_ca_cert = caFile
        client.Configuration.set_default(kube_config)
    elif os.path.exists(test_config):
        config.load_kube_config(test_config)
    else:
        log.error('Kubernetes credentials not found.')
        exit(1)

def construct_ingress_obj(data):
    ingress = {}
    ingress['name'] = data['metadata']['name']
    ingress['namespace'] = data['metadata']['namespace']
    for rule in data['spec']['rules']:
        ingress['host'] = rule['host']
        for path in rule['http']['paths']:
            ingress['serviceName'] = path['backend']['serviceName']
            ingress['servicePort'] = path['backend']['servicePort']
    return ingress
    
def get_ingress_list():
    get_kube_credentials()
    v1beta1 = client.ExtensionsV1beta1Api()
    response = json.load(v1beta1.list_ingress_for_all_namespaces(_preload_content=False))
    ingress_list = [ construct_ingress_obj(item) for item in response['items'] ]
    return ingress_list

if __name__ == "__main__":
    get_ingress_list()