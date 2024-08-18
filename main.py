from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from constants.constants import ENV_TAVILY_API_KEY, MACHINE_REPO_ID, MACHINE_USER_ID
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging
from services.Analyzer import Analyzer
from services.SupabaseService import SupabaseService
from services.GitHubAnalyzer import GitHubAnalyzer
import os
from dotenv import load_dotenv

# from services.TavilyService import TavilyService
# Load environment variables
load_dotenv()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

github_analyzer = GitHubAnalyzer()  # Instantiate GitHubAnalyzer
# tavily_service = TavilyService()
supabase_service = SupabaseService()


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
        # Get the repository data
        an = Analyzer()
        logger.info(
            f"[main] Starting repo AI workflow with username: {input_data.username} and repository name: {input_data.repository_name}",)
        analysis = an.start_repo_ai_workflow(
            input_data.username, input_data.repository_name)
        logger.info("[main] Analysis completed")
        return {"result": analysis}
    except Exception as e:
        logger.error("[main] Error in analyzeRepository: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
