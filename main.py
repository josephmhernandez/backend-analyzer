from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from constants.constants import ENV_TAVILY_API_KEY
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging
from services.GitHubAnalyzer import GitHubAnalyzer
import os
from dotenv import load_dotenv
from models.event_repo_request import EventRepoRequest
from fastapi.middleware.cors import CORSMiddleware
from services.TavilyService import TavilyService
from services.sse_events import SseEvents
# Load environment variables
load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

github_analyzer = GitHubAnalyzer()  # Instantiate GitHubAnalyzer
tavily_service = TavilyService()
my_events = SseEvents()


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


@app.post("/analyzeRepository")
async def analyze_repository(input_data: GithubRepositoryRequest):
    try:
        # result = await github_analyzer.fetch_repo_details(input_data.username, input_data.repository_name)
        # repo_contents = await github_analyzer.fetch_repo_contents("https://github.com/josephmhernandez/lyfe-captures")
        # aggregated_code = await github_analyzer.aggregate_code(repo_contents)
        aggregated_code = ""
        analysis = await github_analyzer.analyze_code_with_openai(aggregated_code)
        print("Analysis:", analysis)
        # res = tavily_service.get_software_tech_summary(result["url"])
        # res = await github_analyzer.analyze_repo_with_gpt(result)
        # result = await github_analyzer.analyze_repo(input_data)
        logger.info("[main] Repository analyzed for user: %s",
                    input_data.username)
        return {"result": analysis}
    except Exception as e:
        logger.error("[main] Error in analyzeRepository: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/add-event")
async def add_event(event: EventRepoRequest):
    my_events.add_event(event)
    return {"message": "Event added successfully"}


@app.get("/stream-event")
async def stream_event(request: Request):
    # Add an SSE event (Server-Sent Event) to the event stream to process the repository in real time
    # Each event will be on repository and publish the results supabase analysis table
    # Event will have the job_id (supabase), candidate_id (supabase), and the repository url (github)
    # Event will be processed by the worker to analyze the repository
    # Status will be updated in the supabase table when analysis completed
    # complete status, and analysis_id will be sent back to the client (server side of the application though)

    # Get the data from the request
    data = await request.json()
    while

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
