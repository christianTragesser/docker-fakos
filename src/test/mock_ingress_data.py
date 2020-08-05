class MockMetadata(object):
    @property
    def name(self):
        return 'test0'

    @property
    def namespace(self):
        return 'default'


class ServiceMock(object):
    def __init__(self):
        self.service_name = 'test0_web'
        self.service_port = 80


class MockBackend(object):
    @property
    def backend(self):
        return ServiceMock()


class MockHTTP(object):
    def __init__(self):
        self.path_values = [MockBackend()]

    @property
    def paths(self):
        return list(self.path_values)


class MockRules(object):
    def __init__(self):
        self.host = 'test0.io'
        self.http = MockHTTP()


class MockSpec(object):
    def __init__(self):
        self.rules_values = [MockRules()]

    @property
    def rules(self):
        return list(self.rules_values)


class MockIngress(object):
    @property
    def metadata(self):
        return MockMetadata()

    @property
    def spec(self):
        return MockSpec()


class MockItems(list):
    def __init__(self):
        self.ingress_mocks = [MockIngress()]

    def __getitem__(self, index):
        return self.ingress_mocks[index]

    @property
    def items(self):
        return self.ingress_mocks


all_namespace_ingress_items = [
    {
        'metadata': {
            'name': 'test0',
            'namespace': 'default',
        },
        'spec': {
            'rules': [
                {
                    'host': 'test0.io',
                    'http': {
                        'paths': [
                            {
                                'backend': {
                                    'service_name': 'test0_web',
                                    'service_port': 80
                                },
                            }
                        ]
                    }
                }
            ],
        },
    },
    {
        'metadata': {
            'name': 'test1',
            'namespace': 'test1',
        },
        'spec': {
            'rules': [
                {
                    'host': 'test1.io',
                    'http': {
                        'paths': [
                            {
                                'backend': {
                                    'service_name': 'test1_web',
                                    'service_port': 80
                                },
                            }
                        ]
                    }
                }
            ],
        },
    },
    {
        'metadata': {
            'name': 'test2',
            'namespace': 'test2',
        },
        'spec': {
            'rules': [
                {
                    'host': 'test2.io',
                    'http': {
                        'paths': [
                            {
                                'backend': {
                                    'service_name': 'test2_web',
                                    'service_port': 80
                                },
                            }
                        ]
                    }
                }
            ],
        },
    }
]
