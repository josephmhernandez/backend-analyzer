import json
import uuid
import boto3
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging
from services.SupabaseServiceSqs import SupabaseServiceSqs
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from utils.SecretsManager import SecretsManager

# Load environment variables
load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["https://your-vercel-app.vercel.app"],  # Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint doesn't exist"},
    )


@app.get("/")
@app.get("/health")
def read_root():
    return {"message": "Hello World"}

secrets_manager = SecretsManager(secret_name="prod/repo-analyzer")
supabase_service_sqs = SupabaseServiceSqs(secrets_manager=secrets_manager)

sqs_client = boto3.client('sqs')


def send_message_to_sqs(message_body: dict):
    try:
        # Random message DeduplicationId:
        task_id = str(uuid.uuid4())
        # add taskId to message body as string
        message_body["taskId"] = task_id
        QUEUE_URL = secrets_manager.get("sqs.queue.url")

        # Messages with the same message group ID will be ordered in a FIFO manner.
        message_group_id = task_id

        # Send a message
        response = sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            # Convert the message to a JSON string
            MessageBody=json.dumps(message_body),
            MessageGroupId=message_group_id,
            MessageDeduplicationId=f"{task_id}"
        )
        message_id = response['MessageId']
        logging.info(f"Message sent! Message ID: {message_id}")

        # Want to return the unique task id. This will be the queue_task_id in the tasks table
        return task_id
    except Exception as e:
        logging.error(f"Error sending message: {e}")


@app.post("/repository-analysis")
async def submit_analysis_request(input_data: GithubRepositoryRequest, authorization: str = Header(None)):
    logger.info(f"Received request: {input_data}")
    check_api_authorization_sqs(authorization)
    try:
        # Submit to queue.
        logger.info(
            f"Placing task: {input_data} in queue.")
        message = {
            "dbRepoId": input_data.dbRepoId,
            "userId": input_data.userId,
            "repoName": input_data.repoName,
            "repoUrl": input_data.repoUrl
        }
        logger.info(f"Placing message in queue. Message: {message}")
        task_id = send_message_to_sqs(message)
        logger.info(f"Task ID: {task_id}")

        # Insert the task into the database
        res = supabase_service_sqs.insert_task(task_id=task_id)
        if not res:
            raise Exception("Error inserting task into the database")

    except Exception as ex:
        logger.error(f"Error submitting task: {str(ex)}")
        raise HTTPException(
            status_code=500, detail="Error analyzing repository")

    return {"status": "Job submitted successfully", "task_id": task_id}

@app.get("/task/{task_id}/status")
async def get_sqs_task_status(task_id: str):

    # Look up in the supabase db how long the task has been in the Queue. If longer than 5 min then return Failure else PENDING
    # If the task is in the database, then return the status from the database
    response = None

    try:
        task_status = supabase_service_sqs.get_task_status(task_id)

        if task_status == "PENDING":
            response = {"state": "PENDING", "status": "Pending..."}
        elif task_status == "SUCCESS":
            response = {"state": "SUCCESS", "status": "Analysis completed"}
        elif task_status == "FAILURE":
            response = {"state": "FAILURE", "status": "Analysis failed"}
        else:
            response = {"state": task_status, "status": "Unknown status"}

        return response
    except Exception as ex:
        logger.error(f"Error getting task status: {str(ex)}")
        raise HTTPException(
            status_code=500, detail="Error getting task status")


def check_api_authorization(api_key):
    if api_key != os.getenv("SECURE_API_KEY"):
        raise HTTPException(status_code=401, detail="Unauthorized")


def check_api_authorization_sqs(api_key):
    if api_key != secrets_manager.get("secure.api.key"):
        raise HTTPException(status_code=401, detail="Unauthorized")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
