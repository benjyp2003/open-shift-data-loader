# deploy OpenShift Data Loader application
oc apply -f infrastructure\k8s\sql\mysql-secret.yaml
oc apply -f infrastructure\k8s\sql\mysql-pvc.yaml
oc apply -f infrastructure\k8s\sql\mysql-deployment.yaml
oc apply -f infrastructure\k8s\sql\mysql-service.yaml


# build and push Docker image
docker build -t open-shift-data-loader .
docker tag open-shift-data-loader benjyfeffer/open-shift-data-loader:latest
docker login
docker push benjyfeffer/open-shift-data-loader:latest


# deploy FastAPI application and expose a route to it
oc apply -f infrastructure\k8s\fastapi\fastapi-deployment.yaml
oc apply -f infrastructure\k8s\fastapi\fastapi-service.yaml
oc expose svc/fastapi-service --hostname=fastapi-benjypfeffer-dev.apps.cluster-xyz.com