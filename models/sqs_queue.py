from enum import Enum


class SqsQueue(Enum):
    CANDIDATE = "sqs.candidate.queue.url"
    REPOSITORY = "sqs.queue.url"

    # to string prints the name of enum
    def to_string(self):
        return self.name
