from collections import deque

from models.event_repo_request import EventRepoRequest

class SseEvents:
    def __init__(self):
        self.events = deque()

    def add_event(self, event: EventRepoRequest):
        self.events.append(event)

    def get_event(self):
        if len(self.events) > 0:
            return self.events.popleft()
        return None

    def __len__(self):
        return len(self.events)

    def count(self):
        return len(self.events)
