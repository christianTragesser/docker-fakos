# Fakós (φακός)

Fakós is a request latency monitor for [ Kubernetes ](https://kubernetes.io/) Services with Ingress.

Provided a Kubernetes Ingress exists for a service, Fakós will perform a http request on Ingress host(s) and cluster service URLs then return the response duration via [ Prometheus ](https://prometheus.io/) metrics and logging.
