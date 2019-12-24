import pytest
import sys
import os
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main

statsData = (
    {
        'host_latency': 0.111111,
        'name': 'testy', 
        'namespace': 'test',
        'service_latency': 0.222222,
        'validCertDaysRemaining': 56,
    },
    {
        'host_latency': 0.333333,
        'name': 'test2', 
        'namespace': 'default',
        'service_latency': 0.444444,
        'validCertDaysRemaining': 2,
    },
    {
        'host_latency': 0.555555,
        'name': 'test3', 
        'namespace': 'monitoring',
        'service_latency': 0.666666,
        'validCertDaysRemaining': -2,
    }
)

@mock.patch('ping.measure_requests')
def test_create_endpoint_dictionaries(mock_measure_data_func):
    #takes in a tuple of request status dicts from ping.py
    #return single dict record containing stats for each test status
    mock_measure_data_func.return_value = statsData
    main.record_metrics()
    for record in statsData:
        i = statsData.index(record)
        assert record['name'] == statsData[i]['name']
        assert record['namespace'] == statsData[i]['namespace']
        assert record['host_latency'] == statsData[i]['host_latency']
        assert record['service_latency'] == statsData[i]['service_latency']
        assert record['validCertDaysRemaining'] == statsData[i]['validCertDaysRemaining']