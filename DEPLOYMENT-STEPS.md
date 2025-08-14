# 🚀 Step-by-Step Deployment Guide

This guide shows you how to build, push to DockerHub, and deploy to OpenShift manually without using scripts.

## 🐳 Step 1: Build Docker Image

### 1.1 Build the image locally
```bash
# Make sure you're in the project root directory
cd /c/Users/benjy/PycharmProjects/open-shift-data-loader

# Build the Docker image
docker build -t open-shift-data-loader .
```

### 1.2 Tag the image for DockerHub
```bash
# Replace 'your-username' with your actual DockerHub username
docker tag open-shift-data-loader your-username/open-shift-data-loader:latest

# You can also tag with a specific version
docker tag open-shift-data-loader your-username/open-shift-data-loader:v1.0.0
```

## 📤 Step 2: Push to DockerHub

### 2.1 Login to DockerHub
```bash
docker login
# Enter your DockerHub username and password when prompted
```

### 2.2 Push the image
```bash
# Push the latest tag
docker push your-username/open-shift-data-loader:latest

# Push the version tag (if you created one)
docker push your-username/open-shift-data-loader:v1.0.0
```

## 🔧 Step 3: Update Deployment Files

### 3.1 Update the image name in fastapi-deployment.yaml
Edit `infrastructure/k8s/fastapi-deployment.yaml` and change:
```yaml
image: your-username/open-shift-data-loader:latest
```
to your actual image:
```yaml
image: your-username/open-shift-data-loader:latest
```

### 3.2 Update the database name
In the same file, change:
```yaml
- name: MYSQL_DATABASE
  value: "your_database_name"
```
to your actual database name.

### 3.3 Update the route host
Edit `infrastructure/k8s/fastapi-route.yaml` and change:
```yaml
host: fastapi-your-project.apps.your-cluster.com
```
to your actual OpenShift cluster domain.

## 🚀 Step 4: Deploy to OpenShift

### 4.1 Login to OpenShift
```bash
oc login --token=your-token --server=your-server
# Or use: oc login -u your-username -p your-password --server=your-server
```

### 4.2 Create OpenShift project
```bash
oc new-project fastapi-app --display-name="FastAPI Application" --description="FastAPI server with MySQL backend"
```

### 4.3 Deploy MySQL resources
```bash
# Apply MySQL secret
oc apply -f infrastructure/k8s/sql/mysql-secret.yaml

# Apply MySQL persistent volume
oc apply -f infrastructure/k8s/sql/mysql-pv.yaml

# Apply MySQL persistent volume claim
oc apply -f infrastructure/k8s/sql/mysql-pvc.yaml

# Apply MySQL deployment
oc apply -f infrastructure/k8s/sql/mysql-deployment.yaml

# Apply MySQL service
oc apply -f infrastructure/k8s/sql/mysql-service.yaml
```

### 4.4 Wait for MySQL to be ready
```bash
oc wait --for=condition=ready pod -l app=mysql --timeout=300s
```

### 4.5 Deploy FastAPI application
```bash
# Apply FastAPI deployment
oc apply -f infrastructure/k8s/fastapi-deployment.yaml

# Apply FastAPI service
oc apply -f infrastructure/k8s/fastapi-service.yaml

# Apply FastAPI route
oc apply -f infrastructure/k8s/fastapi-route.yaml
```

### 4.6 Wait for FastAPI pods to be ready
```bash
oc wait --for=condition=ready pod -l app=fastapi-server --timeout=300s
```

## 📊 Step 5: Verify Deployment

### 5.1 Check deployment status
```bash
# Check all resources
oc get all

# Check pods specifically
oc get pods

# Check services
oc get services

# Check routes
oc get routes
```

### 5.2 Check logs
```bash
# Check FastAPI logs
oc logs -l app=fastapi-server

# Check MySQL logs
oc logs -l app=mysql

# Follow logs in real-time
oc logs -f deployment/fastapi-server
```

### 5.3 Access the application
```bash
# Get the route URL
oc get route fastapi-route

# Port forward for testing (if needed)
oc port-forward svc/fastapi-service 8080:80
```

## 🔄 Step 6: Update Application (When Needed)

### 6.1 Update image
```bash
# Method 1: Update deployment directly
oc set image deployment/fastapi-server fastapi-app=your-username/open-shift-data-loader:new-tag

# Method 2: Apply updated YAML
oc apply -f infrastructure/k8s/fastapi-deployment.yaml
```

### 6.2 Rollback if needed
```bash
# Rollback to previous deployment
oc rollout undo deployment/fastapi-server

# Check rollout status
oc rollout status deployment/fastapi-server
```

## 🧹 Step 7: Cleanup (When Needed)

### 7.1 Remove application
```bash
# Delete all resources
oc delete all --selector=app=fastapi-server
oc delete all --selector=app=mysql

# Delete project
oc delete project fastapi-app
```

## 🚨 Troubleshooting Commands

### Check events
```bash
oc get events --sort-by='.lastTimestamp'
```

### Describe resources
```bash
oc describe pod <pod-name>
oc describe service <service-name>
oc describe route <route-name>
```

### Check resource quotas
```bash
oc describe quota
```

### Check project status
```bash
oc status
```

## 📝 Important Notes

1. **Replace placeholders**: Always update `your-username`, database names, and cluster domains
2. **Image registry**: Make sure your OpenShift cluster can access DockerHub
3. **Secrets**: The MySQL password is stored in OpenShift secrets
4. **Networking**: Services communicate using internal service names
5. **Security**: The deployment runs with non-root user and dropped capabilities
