import os
import boto3
import json

class SecretsManager:
    def __init__(self, secret_name, region_name="us-east-1"):
        """
        Initialize SecretsManager to retrieve secrets from AWS Secrets Manager.
        :param secret_name: The name of the secret in AWS Secrets Manager.
        :param region_name: The AWS region where the secret is stored.
        """
        self.secret_name = secret_name
        self.region_name = region_name
        self.secrets = None
        self._load_secrets()

    def _load_secrets(self):
        """
        Load secrets from AWS Secrets Manager and cache them in memory.
        """
        client = boto3.client("secretsmanager", region_name=self.region_name)
        try:
            response = client.get_secret_value(SecretId=self.secret_name)
            self.secrets = json.loads(response["SecretString"])
        except Exception as e:
            raise Exception(
                f"Failed to retrieve secret {self.secret_name}: {str(e)}")

    def get(self, key):
        """
        Retrieve a specific secret by key.
        :param key: The key to retrieve from the secrets.
        :return: The value of the secret key.
        """
        if self.secrets is None:
            raise Exception("Secrets not loaded.")

        secret = self.secrets.get(key)

        if secret is None:
            # Check environment variables
            secret = os.environ.get(key)
            if secret is None:
                raise Exception(
                    f"Secret {key} not found in manager or environment variables.")

        return secret
