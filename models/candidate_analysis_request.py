from pydantic import BaseModel


class CandidateAnalysisRequest(BaseModel):
    candidateId: str
    jobId: str
    userId: str

    def __getitem__(self, item):
        return getattr(self, item)

    # Define string representation of the object
    def __str__(self):
        return f"candidateId: {self.candidateId}, jobId: {self.jobId}, userId: {self.userId}"

    