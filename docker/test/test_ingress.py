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
    #return tuple of ingress details
    with open(testJson) as f:
        test_file = json.load(f)
    test_data = dict(test_file)

    mock_list_ingress_func.return_value = open(testJson, 'r')
    ingressList = ingress.get_ingress_list()
    assert isinstance(ingressList, tuple)
    for item in ingressList:
        i = ingressList.index(item)
        assert ingressList[i]['name'] == test_data['items'][i]['metadata']['name']
        assert ingressList[i]['namespace'] == test_data['items'][i]['metadata']['namespace']
        assert ingressList[i]['serviceName'] == test_data['items'][i]['spec']['rules'][0]['http']['paths'][0]['backend']['serviceName']
        assert ingressList[i]['servicePort'] == test_data['items'][i]['spec']['rules'][0]['http']['paths'][0]['backend']['servicePort']
        assert ingressList[i]['host'] == test_data['items'][i]['spec']['rules'][0]['host']