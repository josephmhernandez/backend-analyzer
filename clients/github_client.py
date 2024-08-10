import logging

import httpx

from constants.constants import GITHUB_API_URL


class GitHubClient:
    def __init__(self, token: str = None):
        self.token = token
        self.logger = logging.getLogger(__name__)

    async def get_repo_detail_links(self, username: str, repository: str):
        # Fetch the repo's for a given user
        url = f"{GITHUB_API_URL}/repos/{username}/{repository}/contents"
        try:
            async with httpx.AsyncClient() as client:
                self.logger.info(
                    "[GitHubClient:get_repo_detail_links] Fetching github data from: %s", url)
                response = await client.get(url)
                response.raise_for_status()
                repo_data = response.json()
                self.logger.info(
                    "[GitHubClient:get_repo_detail_links] Fetched github data: %s", str(repo_data))
                return {
                    "status": response.status_code,
                    "html_url": repo_data.get("html_url"),
                    "clone_url": repo_data.get("clone_url"),
                    "ssh_url": repo_data.get("ssh_url"),
                    "git_url": repo_data.get("git_url"),
                    "svn_url": repo_data.get("svn_url"),
                }
        except httpx.HTTPStatusError as e:
            self.logger.error(
                "[GitHubClient:get_repo_detail_links] Error fetching github data: %s. Repository might not exist", str(e))
            raise e
