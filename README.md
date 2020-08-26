# Fakós (φακός)
[![pipeline status](https://gitlab.com/christianTragesser/fakos/badges/master/pipeline.svg)](https://gitlab.com/christianTragesser/fakos/commits/master)

Fakós is a request latency monitor for [ Kubernetes ](https://kubernetes.io/) Services with Ingress.

### Request Latency Metrics
For each Kubernetes Ingress in a cluster(or namespace), Fakós measures the duration of http requests for Ingress and Service endpoints. Metrics are reported via [ Prometheus ](https://prometheus.io/) exporter and Pod logging.

#### Service vs Ingress Metrics
Fakós measures application response latencies using two different perspectives:
 * Kubernetes Service - HTTP request to the local cluster service name `<service name>.<namespace>.svc.cluster.local`

 *  Kubernetes Ingress - HTTPS request to the external `Host` URL defined in an ingress object

 Using the Kubernetes Service metric as a _cluster native_ baseline,  the Kubernetes Ingress metric can then be used to assess ingress infrastructure performance and availability.

 Each service and ingress request provides [ Prometheus Gauge and Histogram metrics ](https://prometheus.io/docs/concepts/metric_types/).


### Certificate Expiration Metrics
Fakós assumes each Ingress endpoint is secured via TLS communications and provides _valid certificate age_ as a metric(Gauge) for tracking certificate renewal cadences.


### Installation
Fakós is available for installation via [Helm package](https://helm.sh/).  
Add the `ctt` repo to Helm:  
```
helm repo add ctt https://helm.evoen.net
```  

For cluster-wide ingress observation:  
```
helm install fakos-metrics ctt/fakos --namespace=kube-system
```  

To restrict Fakós ingress observation to a specific namespace:  
```
helm install fakos-metrics ctt/fakos --namespace=<desired namespace>
```


### Configure Options
**Check Interval**  
By default measurements are taken in 30 minute intervals.  Measurement cadence can be changed by setting the enviromental variable `INTERVAL` in units of minutes.
```sh
# 1 hour interval
helm upgrade fakos-metrics ctt/fakos --set fakos.interval=60 --namespace=kube-system
```  

You can also reference the [ example values file ](https://github.com/christianTragesser/fakos/blob/master/helm/fakos/values.yaml) for further customization using Helm.  