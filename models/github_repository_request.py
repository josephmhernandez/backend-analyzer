from pydantic import BaseModel


class GithubRepositoryRequest(BaseModel):
    dbRepoId: str
    userId: str
    repoName: str
    repoUrl: str

    def __getitem__(self, item):
        return getattr(self, item)

    # Define string representation of the object
    def __str__(self):
        return f"dbRepoId: {self.dbRepoId}, userId: {self.userId}, repoName: {self.repoName}, repoUrl: {self.repoUrl}"
