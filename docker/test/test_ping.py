import pytest
import responses
import sys
import os
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingress
import ping

listExample = [{'host': 'test.io', 'serviceName': 'testem', 'namespace': 'test', 'name': 'testy', 'servicePort': 3000}]

@mock.patch('ingress.getIngressList')
def test_create_endpoint_objects(mock_ingress_data_func):
    #takes in a list of ingress dicts from ingress.py
    #construct service URL(s)
    #construct host URL(s)
    #return array of dicts containing host and service URLs
    mock_ingress_data_func.return_value = listExample
    urlObjects = ping.constructURLs()
    assert urlObjects[0]['name'] == 'testy'
    assert urlObjects[0]['service'] == 'http://testem.test.svc.cluster.local:3000'
    assert urlObjects[0]['host'] == 'https://test.io'
    assert urlObjects[0]['namespace'] == 'test'

@responses.activate
@mock.patch('ingress.getIngressList')
def test_request_url_enpoints(mock_ingress_data_func):
    #takes in list of URL dicts
    #perform http/https request against URL
    #return duration for host and service requests
    mock_ingress_data_func.return_value = listExample
    responses.add(responses.GET, 'https://test.io',
                  status=404)
    responses.add(responses.GET, 'http://testem.test.svc.cluster.local:3000',
                  status=200)

    request_durations = ping.measureRequests()
    assert request_durations[0]['name'] == 'testy'
    assert request_durations[0]['service_latency']
    assert request_durations[0]['host_latency'] == 0
    assert request_durations[0]['namespace'] == 'test'