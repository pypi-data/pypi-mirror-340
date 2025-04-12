from .client import PyroApiClient
from .project import PyroProjectResource
from .job import PyroJobResource
from .job_group import PyroJobGroupResource


class PyroDash:
    """
    Primary entrypoint to pyro-dash resources.
    """

    def __init__(self, host: str, email: str, apikey: str):
        self._client = PyroApiClient(host, email, apikey)
        self.jobs = PyroJobResource(self._client)
        self.projects = PyroProjectResource(self._client)
        self.job_groups = PyroJobGroupResource(self._client)
