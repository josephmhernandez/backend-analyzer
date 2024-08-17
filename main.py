from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from constants.constants import ENV_TAVILY_API_KEY, MACHINE_REPO_ID, MACHINE_USER_ID
from models.github_repository_request import GithubRepositoryRequest
import logging
from logging_config import setup_logging
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
        result = await github_analyzer.fetch_repo_details(input_data.username, input_data.repository_name)
        print("Result of fetch_repo_details:", result)
        # repo_contents = await github_analyzer.fetch_repo_contents("https://github.com/josephmhernandez/lyfe-captures")
        # aggregated_code = await github_analyzer.aggregate_code(repo_contents)
        aggregated_code = ""
        # analysis = await github_analyzer.analyze_code_with_openai(aggregated_code)
        # print("Analysis:", analysis)
        # res = tavily_service.get_software_tech_summary(result["url"])
        analysis = await github_analyzer.analyze_repo_with_gpt(result)
        # result = await github_analyzer.analyze_repo(input_data)
        logger.info("[main] Repository analyzed for user: %s",
                    input_data.username)

        sb_response = await supabase_service.insert_repo_analysis(
            repository_id=MACHINE_REPO_ID,
            created_by=MACHINE_USER_ID,
            summary=analysis["summary"],
            title=input_data.repository_name,
            username=input_data.username,
            repo_url=result["url"],
            problem_statement=analysis["problem_statement"],
            recency_description=analysis["recency_description"],
            demo_description=analysis["demo_description"],
            technologies_description=analysis["technologies_description"],
            techniques_description=analysis["techniques_description"],
            critics_description=analysis["critics_description"]
        )
        logger.info(
            "[main] Inserted repository analysis into supabase: %s", sb_response)

        return {"result": analysis}
    except Exception as e:
        logger.error("[main] Error in analyzeRepository: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
