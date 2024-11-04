import logging
from celery_app import celery_app
from services.Analyzer import Analyzer
from services.SupabaseService import SupabaseService
from services.GitHubHelper import extract_github_info
from models.github_repository_request import GithubRepositoryRequest

from dotenv import load_dotenv
from celery.exceptions import MaxRetriesExceededError

load_dotenv()

logger = logging.getLogger(__name__)
supabase_service = SupabaseService()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def long_running_job_analyze_repo(self, input_data_dict):
    try:
        input_data = GithubRepositoryRequest(**input_data_dict)
        logger.info(f"[tasks] Analyzing repository for: {input_data}")

        # Get the repository data
        username, repository_name = extract_github_info(input_data.repoUrl)

        if not username or not repository_name:
            raise Exception("Invalid GitHub repository URL")

        an = Analyzer()
        logger.info(
            f"Starting repo AI workflow with username: {username} and repository name: {repository_name}")
        analysis = an.start_repo_ai_workflow(username, repository_name)
        logger.info("Analysis completed")

        # Insert the analysis into the database
        logger.info("Inserting analysis into the database")
        res = supabase_service.insert_repo_analysis(
            input_data.dbRepoId,
            input_data.userId,
            analysis["summary"],
            analysis["title"],
            analysis["user"],  # GitHub username
            analysis["repo_url"],
            analysis["problem_statement"],
            analysis["recency_description"],
            analysis["demo_description"],
            analysis["technologies_description"],
            analysis["techniques_description"],
            analysis["critics_description"],
        )
        logger.info(f"[tasks] Supabase response: {res}")
        logger.info("[tasks] Analysis inserted into the database")
        return {"status": "success"}
    except Exception as ex:
        logger.error(f"[tasks] Error analyzing repository: {str(ex)}")

        # If there is an error, try to retry the task
        try:
            raise self.retry(exc=ex)
        except MaxRetriesExceededError as retry_error:
            logger.error(f"Max retries exceeded for task {self.request.id}")
            logger.error(f"Retry error: {str(retry_error)}")

            # Insert error into the database
            try:
                res = supabase_service.insert_repo_analysis(
                    input_data.dbRepoId,
                    input_data.userId,
                    "Error creating analysis. We're looking into it.",
                    input_data.repoName,
                    "",
                    input_data.repoUrl,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                )
            except Exception as db_insert_error:
                logger.error(
                    f"[tasks] Error inserting error into the database: {str(db_insert_error)}")
                raise Exception(
                    "Error in analysis and error inserting into the database")

            logger.error(
                f"Error analyzing this repository. Error inputted into analysis DB table: {input_data.dbRepoId}")
            raise ex
