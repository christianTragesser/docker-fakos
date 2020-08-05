import os
import sys
from unittest import mock
import kubernetes
import mock_ingress_data
from mock_ingress_data import MockItems
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingress


@mock.patch.object(kubernetes.client.ExtensionsV1beta1Api, 'list_ingress_for_all_namespaces', autospec=True)
def test_get_ingress_for_all_namespaces(mock_ingress_list_call):
    # query k8s API for list of ingress
    # construct data structure of ingress data to work with
    # return tuple of dictionaries containing ingress data
    test_data = mock_ingress_data.all_namespace_ingress_items
    mock_ingress_list_call.return_value = MockItems()

    ingress_list = ingress.get_ingress_list()
    assert isinstance(ingress_list, tuple)
    assert ingress_list[0]['name'] == test_data[0]['metadata']['name']
    assert ingress_list[0]['namespace'] == test_data[0]['metadata']['namespace']
    assert ingress_list[0]['host'] == test_data[0]['spec']['rules'][0]['host']
    assert ingress_list[0]['serviceName'] == test_data[0]['spec']['rules'][0]['http']['paths'][0]['backend']['service_name']
    assert ingress_list[0]['servicePort'] == test_data[0]['spec']['rules'][0]['http']['paths'][0]['backend']['service_port']
