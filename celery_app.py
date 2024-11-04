import os

import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv(
    'CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# broker_use_ssl = {
#     'ssl_cert_reqs': 'none'
# }

# redis_backend_use_ssl = {
#     'ssl_cert_reqs': 'none'
# }

celery_app = Celery(
    'backend_analyzer',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    # broker_use_ssl=broker_use_ssl,
    # redis_backend_use_ssl=redis_backend_use_ssl,
    include=['tasks']
)

# Optional configuration, see the application user guide.
celery_app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    celery_app.start()
