from pydantic import BaseModel


class RepositoryAnalyzerResponse(BaseModel):
    summary: dict
    users: dict
    current_state: dict
    software_tools: dict
    software_best_practices: dict
    software_opportunities: dict

    def __getitem__(self, item):
        return getattr(self, item)
