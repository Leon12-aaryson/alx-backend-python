# Kubernetes Deployment Guide for Django Messaging App

This guide explains how to deploy and manage your Django messaging app on Kubernetes using the provided scripts.

## Prerequisites

- Docker installed and running
- At least 4GB RAM and 2 CPU cores available
- Internet connection for downloading Kubernetes components

## Task Overview

1. **Task 0**: Install Kubernetes and Set Up Local Cluster
2. **Task 1**: Deploy Django App on Kubernetes
3. **Task 2**: Scale the Django App
4. **Task 3**: Set Up Kubernetes Ingress
5. **Task 4**: Implement Blue-Green Deployment
6. **Task 5**: Apply Rolling Updates

## Step-by-Step Execution

### Step 1: Set Up Kubernetes Cluster

```bash
# Make script executable and run it
chmod +x kurbeScript
./kurbeScript
```

This script will:
- Install minikube and kubectl if not present
- Start a local Kubernetes cluster
- Verify the cluster is running
- Show cluster status and available pods

**Expected Output**: You should see cluster information and status messages.

### Step 2: Build and Deploy Django App

Before deploying, you need to build your Docker image:

```bash
# Build the Docker image
docker build -t django-messaging-app:latest .

# For blue-green deployment, also build a green version
docker build -t django-messaging-app:green .
docker build -t django-messaging-app:2.0 .
```

Then deploy using the blue deployment:

```bash
# Apply the blue deployment
kubectl apply -f blue_deployment.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

### Step 3: Scale the Application

```bash
# Make script executable and run it
chmod +x kubctl-0x01
./kubctl-0x01
```

This script will:
- Scale the app to 3 replicas
- Verify multiple pods are running
- Perform load testing with wrk
- Monitor resource usage

### Step 4: Set Up Ingress

```bash
# Follow the commands in commands.txt
# Or run these commands manually:

# Install Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Wait for controller to be ready
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Enable minikube ingress addon
minikube addons enable ingress

# Apply ingress configuration
kubectl apply -f ingress.yaml
```

### Step 5: Blue-Green Deployment

```bash
# Make script executable and run it
chmod +x kubctl-0x02
./kubctl-0x02
```

This script will:
- Deploy both blue and green versions
- Set up traffic routing
- Check for errors in the new version
- Test both services

### Step 6: Rolling Updates

```bash
# Make script executable and run it
chmod +x kubctl-0x03
./kubctl-0x03
```

This script will:
- Apply the updated deployment (image version 2.0)
- Monitor rollout progress
- Test for downtime during updates
- Verify update completion

## File Structure

```
messaging_app/
├── kurbeScript              # Task 0: Kubernetes setup
├── blue_deployment.yaml     # Task 1: Blue deployment
├── kubctl-0x01             # Task 2: Scaling script
├── ingress.yaml             # Task 3: Ingress configuration
├── commands.txt             # Task 3: Ingress commands
├── green_deployment.yaml    # Task 4: Green deployment
├── kubeservice.yaml         # Task 4: Service configuration
├── kubctl-0x02             # Task 4: Blue-green script
├── kubctl-0x03             # Task 5: Rolling update script
└── KUBERNETES_README.md     # This file
```

## Troubleshooting

### Common Issues

1. **minikube start fails**: Ensure Docker is running and you have sufficient resources
2. **Pods stuck in Pending**: Check resource availability with `kubectl describe pod <pod-name>`
3. **Image pull errors**: Ensure Docker images are built locally or available in a registry
4. **Ingress not working**: Verify the ingress controller is running with `kubectl get pods -n ingress-nginx`

### Useful Commands

```bash
# Check cluster status
kubectl cluster-info

# View all resources
kubectl get all

# Check pod logs
kubectl logs <pod-name>

# Describe resources for debugging
kubectl describe pod <pod-name>
kubectl describe service <service-name>

# Access minikube dashboard
minikube dashboard

# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

## Testing Your Deployment

After deployment, you can test your app:

```bash
# Port forward to access the service
kubectl port-forward service/django-messaging-service 8080:80

# Test in another terminal
curl http://localhost:8080/
```

## Cleanup

To clean up all resources:

```bash
# Delete all deployments and services
kubectl delete -f blue_deployment.yaml
kubectl delete -f green_deployment.yaml
kubectl delete -f kubeservice.yaml
kubectl delete -f ingress.yaml

# Stop minikube
minikube stop
minikube delete
```

## Notes

- All scripts include error checking and will exit if prerequisites are not met
- The scripts are designed to be run in sequence
- Resource limits are set conservatively for local development
- For production use, adjust resource limits and security settings accordingly
