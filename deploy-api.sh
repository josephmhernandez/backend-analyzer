#!/bin/bash
echo "Logging in to ECR"
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 893278372622.dkr.ecr.us-east-1.amazonaws.com

echo "Get requirements file"
pip freeze > requirements.txt

echo "Building image"
docker build -t candidate-analyzer/backend-api .

echo "Tagging image"
docker tag candidate-analyzer/backend-api:latest 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-api:latest

echo "Pushing image to ECR"
docker push 893278372622.dkr.ecr.us-east-1.amazonaws.com/candidate-analyzer/backend-api:latest

