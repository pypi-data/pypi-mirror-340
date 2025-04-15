"""Process resource."""

import logging
from time import sleep, time

from resdk.exceptions import ResolweServerError

from .base import BaseResource


class BackgroundTask(BaseResource):
    """Background task resource.

    :param resolwe: Resolwe instance
    :type resolwe: Resolwe object
    :param model_data: Resource model data

    """

    endpoint = "task"

    READ_ONLY_FIELDS = BaseResource.READ_ONLY_FIELDS + (
        "started",
        "finished",
        "status",
        "description",
        "output",
    )
    WRITABLE_FIELDS = ()

    def __init__(self, resolwe, **model_data):
        """Initialize attributes."""
        self.logger = logging.getLogger(__name__)

        #: started
        self.started = None
        #: finished
        self.finished = None
        #: status - Possible values:
        #: WA (waiting)
        #: PR (processing)
        #: OK (done)
        #: ER (error)
        self.status = None
        #: description
        self.description = None
        #: output - JSON field, the actual value depends on the background task
        self.output = None

        super().__init__(resolwe, **model_data)

    @property
    def completed(self) -> bool:
        """Return True if the task is completed, False otherwise."""
        return self.status in ["OK", "ER"]

    def wait(self, timeout: float = 0) -> "BackgroundTask":
        """Wait for the background task to finish.

        The task status is retrieved every second.

        :attr timeout: how many seconds to wait for task to finish (0 to wait forever).

        :raise RuntimeError: when the task in not completed within the given timeout

        :return: the finished background task.
        """
        start = time()
        while (timeout == 0 or time() - start < timeout) and not self.completed:
            sleep(1)
            self.update()
        if not self.completed:
            raise RuntimeError(f"Waiting for taks {self.id} timeout.")
        return self

    def result(self, timeout: float = 0, final_statuses=["OK"]):
        """Wait fot the background tast to finish and return its result.

        :attr timeout: how many seconds to wait for task to finish (0 to wait forever).
        :attr final_statuses: return the result when task status is in the list.

        :raise RuntimeError: when the task in not completed within the given timeout
        :raise ResolweServerError: when task state is is not in final statuses.

        :return: the output of the background task.
        """
        self.wait(timeout)
        if self.status not in final_statuses:
            raise ResolweServerError(
                f"Task status {self.status} not in {final_statuses} ({self.output})."
            )
        return self.output
