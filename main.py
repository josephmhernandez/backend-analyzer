import json
import uuid
import boto3
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging

from services.SupabaseService import SupabaseService

from dotenv import load_dotenv

from utils.SecretsManager import SecretsManager
from fastapi.middleware.cors import CORSMiddleware


# from services.TavilyService import TavilyService
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

# github_analyzer = GitHubAnalyzer()  # Instantiate GitHubAnalyzer
# tavily_service = TavilyService()
secrets_manager = SecretsManager(secret_name="prod/repo-analyzer")
supabase_service = SupabaseService(secrets_manager=secrets_manager)

sqs_client = boto3.client('sqs')


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


def send_message_to_sqs(message_body: dict):
    try:
        # Random message DeduplicationId:
        task_id = str(uuid.uuid4())
        # add taskId to message body as string
        message_body["taskId"] = task_id
        QUEUE_URL = secrets_manager.get("sqs.queue.url")
        # Send a message
        response = sqs_client.send_message(
            QueueUrl=QUEUE_URL,
            # Convert the message to a JSON string
            MessageBody=json.dumps(message_body),
            MessageGroupId="JobAnalysisGroup",
            MessageDeduplicationId=f"{task_id}"
        )
        message_id = response['MessageId']
        logger.info(f"Message sent! Message ID: {message_id}")

        return message_id
    except Exception as e:
        print(f"Error sending message: {e}")


@app.post("/analyze-repository")
async def analyze_repository(input_data: GithubRepositoryRequest, authorization: str = Header(None)):

    # Create a task_id and submit to the queue. The task_id will be logged and returned to the client to be stored in teh repositories analysis table.
    # Put the task_id in the Tasks Supabase Table with a status of PENDING.

    # Generate uuid for

    check_api_authorization(authorization)
    try:
        # Submit to queue.
        logger.info(
            f"Placing task: {input_data} in queue: ")
        message = {
            "dbRepoId": input_data.dbRepoId,
            "userId": input_data.userId,
            "repoName": input_data.repoName,
            "repoUrl": input_data.repoUrl
        }
        task_id = send_message_to_sqs(message)
        logger.info(f"Task ID: {task_id}")

        # Insert the task into the database
        res = supabase_service.insert_task(task_id=task_id)

    except Exception as ex:
        logger.error(f"Error submitting task: {str(ex)}")
        raise HTTPException(
            status_code=500, detail="Error analyzing repository")

    return {"status": "Job submitted successfully", "task_id": task_id}

    # check_api_authorization(authorization)
    # try:
    #     input_data_dict = input_data.dict()

    #     # Enqueue the task
    #     logger.info(
    #         f"Placing task: {input_data_dict} in queue: {os.getenv('CELERY_BROKER_URL')}")
    #     task = long_running_job_analyze_repo.delay(input_data_dict)
    #     logger.info(f"Task ID: {task.id}")
    # except Exception as ex:
    #     logger.error(f"Error submitting task: {str(ex)}")
    #     raise HTTPException(
    #         status_code=500, detail="Error analyzing repository")
    # # Optionally return the task ID
    return {"status": "Job submitted successfully", "task_id": task.id}


@app.get("/tasks/{task_id}/status")
async def get_task_status(task_id: str):

    # Look up in the supabase db how long the task has been in the Queue. If longer than 5 min then return Failure else PENDING
    # If the task is in the database, then return the status from the database
    response = None

    try:
        task_status = supabase_service.get_task_status(task_id)
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
    if api_key != secrets_manager.get("secure.api.key"):
        raise HTTPException(status_code=401, detail="Unauthorized")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
