from unittest import mock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ping

list_example = ({'host': 'test.local', 'serviceName': 'testem', 'namespace': 'test', 'name': 'testy', 'servicePort': 3000},)
obj_example = {'name': 'testy', 'namespace': 'test', 'host': 'https://test.local', 'service': 'http://testem.test.svc.cluster.local:3000'}
duration_example = [{'service_latency': 0.000551, 'host_latency': -1, 'name': 'testy', 'namespace': 'test'}]
url_object_example = {'host': 'test.local', 'serviceName': 'testem', 'namespace': 'test', 'name': 'testy', 'servicePort': 3000, 'service': 'testem.test.svc.cluster.local:3000'}


@mock.patch('ingress.get_ingress_list')
def test_create_endpoint_objects(mock_ingress_data_func):
    # takes in a tuple of ingress dicts from ingress.py
    # construct service URL(s)
    # construct host URL(s)
    # return tuple of dicts containing host and service URLs
    mock_ingress_data_func.return_value = list_example
    urlObjects = ping.construct_endpoints()
    assert isinstance(urlObjects, tuple)
    assert urlObjects[0]['name'] == 'testy'
    assert urlObjects[0]['service'] == 'testem.test.svc.cluster.local:3000'
    assert urlObjects[0]['host'] == 'test.local'
    assert urlObjects[0]['namespace'] == 'test'


@mock.patch('ssl_check.cert_days_remaining', return_value=22)
@mock.patch('ping.get_request_duration', return_value=2)
def test_construct_results(mock_request_duration, mock_ssl_check):
    results = ping.construct_results(url_object_example)
    assert results['name'] == 'testy'
    assert results['namespace'] == 'test'
    assert results['service_latency'] == 2
    assert results['host_latency'] == 2
    assert results['cert_expire_days'] == 22


@mock.patch('ssl_check.cert_days_remaining', return_value=56)
@mock.patch('ping.get_request_duration')
def test_log_metrics(mock_reqs_dur_data, mock_ssl_check, caplog):
    mock_reqs_dur_data.return_value = duration_example
    ping.construct_results(obj_example)
    assert duration_example[0]['name'] in caplog.text
    assert str(duration_example[0]['service_latency']) in caplog.text
    assert str(duration_example[0]['host_latency']) in caplog.text
    assert duration_example[0]['namespace'] in caplog.text
    assert str(mock_ssl_check.return_value) in caplog.text


exception_message = 'testing exception handling'


@mock.patch('ssl_check.get_not_after_date', side_effect=Exception(exception_message))
@mock.patch('ping.get_request_duration')
def test_certs_error(mock_reqs_dur_data, mock_ssl_check, caplog):
    # prints TLS certificate errors to log stream
    mock_reqs_dur_data.return_value = duration_example
    ping.construct_results(obj_example)
    assert duration_example[0]['name'] in caplog.text
    assert str(duration_example[0]['service_latency']) in caplog.text
    assert str(duration_example[0]['host_latency']) in caplog.text
    assert duration_example[0]['namespace'] in caplog.text
    assert "A certificate check is failing, https://test.local is not valid:" in caplog.text
    assert "testing exception handling" in caplog.text
    assert "'cert_expire_days': -1" in caplog.text
