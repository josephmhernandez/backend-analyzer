#!/bin/bash
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 893278372622.dkr.ecr.us-east-1.amazonaws.com

echo "Get requirements file"
pipenv requirements > requirements.txt

echo "Building images"
echo "Building api image"
docker build -f Dockerfile.api -t candidate-analyzer/backend-analyzer-api:latest .
echo "Building worker image"
docker build -f Dockerfile.worker -t candidate-analyzer/backend-analyzer-worker:latest .

echo "Tagging images...."

echo "Tagging & pushing api image"
docker tag candidate-analyzer/backend-analyzer-api:latest 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-analyzer-api:latest
docker push 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-analyzer-api:latest

echo "Tagging & pushing worker image"
docker tag candidate-analyzer/backend-analyzer-worker:latest 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-analyzer-worker:latest
docker push 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-analyzer-worker:latest
