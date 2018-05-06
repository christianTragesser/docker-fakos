# fakós (φακός)

Fakós is a request latency monitor for [ Kubernetes ](https://kubernetes.io/) Services accessed via Ingress.

## Dependencies
The Fakós docker container is a single component of a larger observabilty solution.

* The Fakós container must be run as a Kubernetes Service using a RBAC defined system account.
* Metrics are currently exported explicitly for the [ Prometheus monitoring system and time-series database. ](https://prometheus.io/) 
