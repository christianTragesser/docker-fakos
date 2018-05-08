import pytest
import sys
import os
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fakos

statsData = [
    {
        'host_latency': 0.111111,
        'name': 'testy', 
        'namespace': 'test',
        'service_latency': 0.222222,
    },
    {
        'host_latency': 0.333333,
        'name': 'test2', 
        'namespace': 'default',
        'service_latency': 0.444444,
    },
    {
        'host_latency': 0.555555,
        'name': 'test3', 
        'namespace': 'monitoring',
        'service_latency': 0.666666,
    }
]

@mock.patch('ping.measureRequests')
def test_create_endpoint_objects(mock_stats_data_func, caplog):
    #takes in a list of request status dicts from ping.py
    #construct log dict
    #return single dict record for each status
    mock_stats_data_func.return_value = statsData
    fakos.recordMetrics()
    for record in statsData:
        assert record['name'] in caplog.text
        assert record['namespace'] in caplog.text
        assert str(record['host_latency']) in caplog.text
        assert str(record['service_latency']) in caplog.text