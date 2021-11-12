import time

INCOMPLETE_STATES = set(["CREATED", "STARTING", "RUNNING"])


class BaseTask:
    def __init__(self, response, get_method):
        self.response = response
        self.get_method = get_method

    def result(self):
        while self.response["status"] in INCOMPLETE_STATES:
            self.response = self.get_method(self.response["id"])
            time.sleep(5)
        return self.response