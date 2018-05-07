# fakós (φακός)

Fakós is a request latency monitor for [ Kubernetes ](https://kubernetes.io/) Services with Ingress.

## Dependencies
The Fakós docker container is a single component of a larger observabilty solution.

* The Fakós container must be run by an RBAC defined service account as a Kubernetes Service.
* Metrics are currently presented by [ Prometheus Exporter ](https://prometheus.io/) and system logs.
