# Fakós (φακός)

Fakós is a request latency monitor for [ Kubernetes ](https://kubernetes.io/) Services with Ingress.

For each Kubernetes Ingress in a cluster(or namespace), Fakós measures the duration of http requests for Ingress and Service URLs. Metrics are reported via [ Prometheus ](https://prometheus.io/) exporter and Pod logging.
