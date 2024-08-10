import logging
import os
from tavily import TavilyClient, UsageLimitExceededError

from constants.constants import ENV_TAVILY_API_KEY


class TavilyService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = TavilyClient(os.getenv(ENV_TAVILY_API_KEY))

    def get_software_tech_summary(self, repository_name: str):
        prompt = (
            f"Search the source code of this github repository: {{'repo_url': {repository_name}}} and summarize the software technologies used. I want look at the languages, frameworks, libraries, and tools used in the project. Include programming languages, frameworks, libraries, cloud providers, cloud components, database types, cache types, and other software components utilized in this application."
        )
        self.logger.info(
            "[TavilyService:get_software_tech_summary] using prompt: %s", prompt)

        try:
            response = self.client.get_search_context(prompt)
            return response
        except UsageLimitExceededError:
            self.logger.error(
                "[TavilyService:get_software_tech_summary] Usage limit exceeded for Tavily API")
            raise Exception("Usage limit exceeded for Tavily API")
        except Exception as e:
            self.logger.error(
                "[TavilyService:get_software_tech_summary] Error fetching software tech summary: %s", str(e))
            raise e
