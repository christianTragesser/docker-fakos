import pytest
import os
import sys
import json
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingress

dirPath = os.path.dirname(os.path.realpath(__file__))
testJson = dirPath+'/multi.json'

@mock.patch('kubernetes.client.ExtensionsV1beta1Api.list_ingress_for_all_namespaces')
def test_get_ingress_objects(mock_list_ingress_func):
    #query k8s ingress API
    #return list of ingress details
    mock_list_ingress_func.return_value = open(testJson, 'r')
    ingressList = ingress.getIngressList()
    assert ingressList[0]['name'] == 'testy'
    assert ingressList[0]['namespace'] == 'test'
    assert ingressList[0]['serviceName'] == 'testem'
    assert ingressList[0]['servicePort'] == 3000
    assert ingressList[0]['host'] == 'test.io'
    assert ingressList[1]['name'] == 'test2'
    assert ingressList[1]['namespace'] == 'default'
    assert ingressList[1]['serviceName'] == 'test2em'
    assert ingressList[1]['servicePort'] == 9093
    assert ingressList[1]['host'] == 'test2.test.io'
    assert ingressList[2]['name'] == 'test3'
    assert ingressList[2]['namespace'] == 'monitoring'
    assert ingressList[2]['serviceName'] == 'test3em'
    assert ingressList[2]['servicePort'] == 80
    assert ingressList[2]['host'] == 'test3.test.io'
