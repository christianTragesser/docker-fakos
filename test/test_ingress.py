import pytest
import os
import sys
import json
import mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ingress

ingressSample = {
  "items": [
    {
      "metadata": {
        "name": "testy",
        "namespace": "test"
      },
      "spec": {
        "rules": [
          {
            "host": "test.io",
            "http": {
              "paths": [
                {
                  "backend": {
                    "serviceName": "testem",
                    "servicePort": 80
                  },
                  "path": "/"
                }
              ]
            }
          }
        ]
      }
    }
  ]
}

@mock.patch('kubernetes.client.ExtensionsV1beta1Api.list_ingress_for_all_namespaces')
def test_get_ingress_objects(mock_list_ingress_func):
    mock_list_ingress_func.return_value = json.dumps(ingressSample)
    ingressList = ingress.getIngressList()
    assert ingressList[0]['name'] == 'testy'
    assert ingressList[0]['namespace'] == 'test'
    assert ingressList[0]['serviceName'] == 'testem'
    assert ingressList[0]['host'] == 'test.io'