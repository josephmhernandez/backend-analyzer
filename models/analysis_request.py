from pydantic import BaseModel

from models.github_repository_request import GithubRepositoryRequest


# List of GithubRepositoryRequest
class AnalysisRequest(BaseModel):
    analysisRequest: list[GithubRepositoryRequest]

    def __getitem__(self, item):
        return getattr(self, item)

    # Define string representation of the object
    def __str__(self):
        return f"analysisRequest: {self.analysisRequest}"
