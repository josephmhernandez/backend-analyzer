from pydantic import BaseModel


class GithubRepositoryRequest(BaseModel):
    username: str
    repository_name: str

    def __getitem__(self, item):
        return getattr(self, item)
