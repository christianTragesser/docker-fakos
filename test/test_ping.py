import pytest
import sys
import os
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingress
import ping

listExample = [{'host': 'test.io', 'serviceName': 'testem', 'namespace': 'test', 'name': 'testy'}]

@mock.patch('ingress.getIngress')
def test_create_enpoint_objects(mock_ingress_data_func):
    #takes in a list of ingress dicts from ingress.py
    #construct service URL(s)
    #construct host URL(s)
    #return array of dicts containing host and service URLs
    mock_ingress_data_func.return_value = listExample
    ingressData = ingress.getIngress()
    urlObjects = ping.constructURL()
    assert urlObjects[0]['service'] == 'http://testem.test.svc.cluster.local'
    assert urlObjects[0]['host'] == 'https://test.io'