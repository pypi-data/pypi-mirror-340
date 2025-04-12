from __future__ import annotations
from typing import Optional, Union
from dataclasses import dataclass

from .core import GET, POST, require_resource
from .job import PyroJob, PyroJobResource
from .client import PyroApiClient


class PyroJobGroupResource:
    def __init__(self, client: PyroApiClient):
        self.client = client
        self._endpoint = "job_groups"

    @classmethod
    def from_client(cls, client: PyroApiClient) -> "PyroJobGroupResource":
        return PyroJobGroupResource(client)

    def create(self, name: str = "Untitled Group") -> PyroJobGroup:
        """
        # Create a job group

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.create("PY999")
        ```
        """
        resp = self.client.request(POST, self._endpoint, {"name": name})
        _dict = {**resp, "_resource": self}
        return PyroJobGroup.from_dict(_dict)

    def list_jobs(self, id: str) -> list[PyroJob]:
        """
        # Retrieve jobs in a job group

        ## Example
        ```python
        pyro = PyroDash(...)
        job_group_id = "jg_2VF7h.."
        jobs = pyro.job_groups.list_jobs(job_group_id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        resp = self.client.request(GET, url)
        jobs = []
        for job in resp["jobs"]:
            job_url = f"jobs/{job['id']}"
            full_job_raw = self.client.request(GET, job_url)
            as_dict = {**full_job_raw, "_resource": PyroJobResource(self.client)}
            jobs.append(PyroJob.from_dict(as_dict))

        return jobs

    def add_job(self, id: str, job_id: str) -> PyroJob:
        """
        # Add a job to a job group

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.create()
        job_id = "j_r62X.."
        job = group.add_job(job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/add_job"
        resp = self.client.request(POST, url, {"job_id": job_id})
        _dict = {**resp, "_resource": PyroJobResource(self.client)}
        return PyroJob.from_dict(_dict)

    def create_job(self, id: str, job: Union[PyroJob, dict]) -> PyroJob:
        """
        # Create and add a new job to a job group

        This creates a new job and adds it to the specified job group.

        Note: This does **not** copy the job's config.
        Use `duplicate()` if you want to fully clone a job, or call `update()` after creation.

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.get("g_123")

        # From dict
        job = group.create_job({"type": "fsim", "name": "Test", "description": "A test job"})

        # From existing job
        source_job = pyro.jobs.get("j_r62X..")
        job = group.create_job(source_job)
        ```
        """
        if isinstance(job, PyroJob):
            return self.create_job_from_pyrojob(id, job)
        elif isinstance(job, dict):
            return self.create_job_from_dict(id, job)
        else:
            msg = "source job provided is of unexpected type. cannot create a new job from it."
            raise TypeError(msg)

    def create_job_from_dict(self, id: str, job: dict) -> PyroJob:
        """
        # Create a job from a dictionary and add it to a job group

        The dict must include a `"type"` field. Config is not copied.

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.get("g_123")
        job = group.create_job_from_dict({
            "type": "fsim",
            "name": "My Job",
            "description": "Something useful"
        })
        ```
        """
        if job["type"] is None:
            raise ValueError("dict specified does not have a type!")

        job_rsc = PyroJobResource(self.client)
        new_job = job_rsc.create(job["type"])
        new_job.update(
            name=job.get("name", "Unlabeled"), description=job.get("description", "")
        )

        self.add_job(id, new_job.id)
        return job_rsc.get(new_job.id)

    def create_job_from_pyrojob(self, id: str, job: PyroJob) -> PyroJob:
        """
        # Create a job from another PyroJob and add it to a job group

        Only the job's name and description are copied—not config.

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.get("g_123")
        template_job = pyro.jobs.get("j_r62X..")
        new_job = group.create_job_from_pyrojob(template_job)
        ```
        """
        if job.type is None:
            raise ValueError("job specified does not have a type!")

        job_rsc = PyroJobResource(self.client)
        new_job = job_rsc.create(job.type)  # pyright: ignore
        new_job.update(name=job.name, description=job.description)

        self.add_job(id, new_job.id)
        return job_rsc.get(new_job.id)


@dataclass
class PyroJobGroup:
    id: str
    name: str
    created_at: str
    is_active: str
    _resource: Optional[PyroJobGroupResource] = None

    @classmethod
    def default(cls, **kwargs) -> PyroJobGroup:
        return PyroJobGroup(**kwargs)

    @classmethod
    def from_dict(cls, _dict: dict) -> PyroJobGroup:
        return PyroJobGroup(
            _dict["id"],
            _dict["name"],
            _dict["created_at"],
            _dict["is_active"],
            _dict["_resource"],
        )

    @require_resource
    def list_jobs(self) -> list[PyroJob]:
        """
        # Retrieve jobs in this job group

        ## Example
        ```python
        job_group = PyroJobGroup(...)
        job = job_group.list_jobs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_jobs(self.id)

    @require_resource
    def add_job(self, job_id: str) -> PyroJob:
        """
        # Add a job to this job group

        ## Example
        ```python
        job_group = PyroJobGroup(...)
        job_id = "j_r62X"
        job = job_group.add_job(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.add_job(self.id, job_id)

    @require_resource
    def create_job(self, job: Union[PyroJob, dict]):
        """
        # Create and add a job to this job group

        This creates a new job using the provided PyroJob or dict,
        and adds it to this job group. Config is not copied.

        ## Example
        ```python
        pyro = PyroDash(...)
        group = pyro.job_groups.get("g_123")

        # From dict
        job = group.create_job({"type": "fsim", "name": "Quick Job"})

        # From existing job
        template = pyro.jobs.get("j_r62X")
        job = group.create_job(template)
        ```
        """
        assert self._resource is not None
        return self._resource.create_job(self.id, job)
