from pydantic import BaseModel


class EventRepoRequest(BaseModel):
    username: str
    repository_name: str
    status: str = "pending"
    analysis_id: str = None

    def __getitem__(self, item):
        return getattr(self, item)
