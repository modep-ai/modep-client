import time

INCOMPLETE_STATUSES = set(["CREATED", "STARTING", "RUNNING"])


class BaseTask:
    def __init__(self, response, get_method):
        """
        Initialize a task object, which monitors the status of a task.

        :param dict response: The initial response from the server
        :param function get_method: The method to use to get the task status
        :return: the final response from the server once the task is complete
        """
        self.response = response
        self.get_method = get_method

    def result(self):
        """
        Get the result of the task. This will block until the task is complete.
        """
        while self.response["status"] in INCOMPLETE_STATUSES:
            self.response = self.get_method(self.response["id"])
            time.sleep(5)
        return self.response
