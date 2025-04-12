from dataclasses import dataclass
from typing import Optional, Union, List

from pyro_dash_py.job_group import PyroJobGroup, PyroJobGroupResource
from .client import PyroApiClient
import json
from pyro_dash_py.job import PyroJob, PyroJobResource
from .core import (
    GET,
    POST,
    DEL,
    require_resource,
)


@dataclass
class ProjectFilter:
    field: str
    value: Union[str, float, int]
    op: Optional[str] = "ILIKE"


class PyroProjectResource:
    """
    An interface for projects in the Pyro ecosystem.

    Provides an organization mechanism for Pyro jobs and job groups.
    """

    def __init__(self, client: PyroApiClient):
        self.client = client
        self._endpoint = "projects"

    def create(self, name: Optional[str] = None):
        """
        # Create a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.create("my pyro project")
        print(project.name)
        print(project.id)
        """
        data = {"name": name}
        raw = self.client.request("POST", self._endpoint, data)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def get(self, id: str):
        """
        # Retrieve a project by ID

        ## Example
        ```python
        pyro = PyroDash(...)
        id = "p_3QZ12NDKxyokJiwLbNBM7G"
        project = pyro.pyrojects.get(id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self.client.request("GET", url)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def filter(self, filters: List[ProjectFilter] = [], page=1, num_per_page=10):
        """
        # Retrieve a list of projects

        The projects returned are filtered and paginated in accordance
        with the params you provide. If no filters are provided,
        then all of the projects are retrieved.

        ## Example
        ```python
        pyro = PyroDash(...)

        # Get all of my projects (returns maximum of 20)
        projects = pyro.projects.filter(num_per_page=20)

        # Get all projects that have wildest in the name (not case sensitive)
        filters = [ProjectFilter("name", "wildest")]
        wildest_projects = pyro.projects.filter(filters)
        ```
        """
        params = {
            "page": page,
            "limit": num_per_page,
            "filters": json.dumps([filter.__dict__ for filter in filters]),
        }
        raw = self.client.request("GET", self._endpoint, params)
        projects: List[PyroProject] = []
        for data in raw["data"]:
            _dict = {**data, "_resource": self}
            project = PyroProject.from_dict(_dict)
            projects.append(project)
        return projects

    def find_by_name(self, name: str):
        """
        # Find a project by name

        This function only expects exactly one match. If more or less
        are found, a `ValueError` will be raised.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my project")
        print(project.name)
        >>> "my_project"
        project.list_jobs() # etc
        ```
        """
        projects = self.filter([ProjectFilter("name", name)])
        if len(projects) == 0:
            raise ValueError(f"Cannot find project with name: {name}")
        if len(projects) > 1:
            raise ValueError(f"Name {name} is ambiguous, too many results returned")

        return projects[0]

    def create_job(self, id: str, job: Union[PyroJob, dict]) -> PyroJob:
        """
        # Creates a new job in a project

        Creates a job and handles automatically adding it to a project.

        You can specify either a `PyroJob` or a `dict` as the `job` parameter.
        The system will automatically use the fields in this object to create
        an entirely new job in this project.

        When you specify a `PyroJob` a new job is created that is simply "modelled"
        after that job i.e. using a set of its properties.

        ## Args:
            id (str): project id
            job (Union[PyroJob | dict]): the properties to use when creating the job

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h"
        job = {"type": "fsim", "name": "my fsim job"}
        new_job = pyro.projects.create_job(project_id, job)
        assert new_job.name == "my fsim job"
        ```
        """
        if isinstance(job, PyroJob):
            return self.create_job_from_pyrojob(id, job)
        elif isinstance(job, dict):
            return self.create_job_from_dict(id, job)
        else:
            raise TypeError(
                "source job provided is of unexpected type. cannot create a new job from it."
            )

    def create_job_from_dict(self, id: str, job: dict) -> PyroJob:
        """
        # Create a new job in a project (from a dictionary)

        ## Args:
            id (str): project id
            job (dict): the dictionary to use when creating the job

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h"
        job = {"type": "fsim", "name": "my fsim job"}
        new_job = pyro.projects.create_job_from_dict(project_id, job)
        assert new_job.name == "my fsim job"
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
        # Create a new job in a project (from a `PyroJob` object)

        ## Args:
            id (str): project id
            job (dict): the dictionary to use when creating the job

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h"
        job = PyroJob("j_r62X", "fsim", ..)
        new_job = pyro.projects.create_job_from_pyrojob(project_id, job)
        ```
        """
        if job.type is None:
            raise ValueError("job specified does not have a type!")

        job_rsc = PyroJobResource(self.client)
        new_job = job_rsc.create(job.type)  # pyright: ignore
        new_job.update(name=job.name, description=job.description)
        self.add_job(id, new_job.id)
        return job_rsc.get(new_job.id)

    def add_job(self, id: str, job_id: str) -> PyroJob:
        """
        # Add a job to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_id = "j_r62X.."
        job = pyro.projects.add_job(project_id, job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/add_job"
        raw = self.client.request(POST, url, {"job_id": job_id})
        _dict = {**raw, "_resource": PyroJobResource(self.client)}
        return PyroJob.from_dict(_dict)

    def add_job_group(self, id: str, job_group_id: str) -> PyroJobGroup:
        """
        # Add job group to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_group_id = "jg_la043"
        job_group = pyro.projects.add_job_group(project_id, job_group_id)
        ```
        """
        url = f"{self._endpoint}/{id}/add_job_group"
        resp = self.client.request(POST, url, {"job_group_id": job_group_id})
        _dict = {**resp, "_resource": PyroJobGroupResource(self.client)}
        return PyroJobGroup.from_dict(_dict)

    def duplicate_job(self, id: str, job_id: str) -> PyroJob:
        """
        # Duplicate a job in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_id = "j_r62X.."
        duplicate_job = pyro.projects.duplicate_job(project_id, job_id)
        ```
        """
        url = f"{self._endpoint}/{id}/duplicate_job"
        raw = self.client.request(POST, url, {"job_id": job_id})
        _dict = {**raw, "_resource": PyroJobResource(self.client)}
        return PyroJob.from_dict(_dict)

    def delete(self, id: str):
        """
        # Delete a project

        Deleting a project will also delete any jobs and data
        associated with it. Tread carefully.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my cringe project")
        pyro.projects.delete(project.id)
        ```
        """
        url = f"{self._endpoint}/{id}"
        raw = self.client.request(DEL, url)
        _dict = {**raw, "_resource": self}
        return PyroProject.from_dict(_dict)

    def list_jobs(self, id: str) -> list[PyroJob]:
        """
        # Retrieves jobs in a project

        This function will return ALL jobs in a project,
        those that are directly associated with a project
        and those that are associated with a project
        through a job group.

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        jobs = pyro.projects.list_jobs(project_id)
        ```
        """
        jobs = self.list_ungrouped_jobs(id)

        # also fetch any jobs that may be in job groups
        # for this project
        job_groups = self.list_job_groups(id)
        for group in job_groups:
            grouped_jobs = group.list_jobs()
            for grouped_job in grouped_jobs:
                jobs.append(grouped_job)

        return jobs

    def list_job_groups(self, id: str) -> list[PyroJobGroup]:
        """
        # Retrieves job groups in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        job_groups = pyro.projects.list_job_groups(project_id)
        ```
        """
        job_groups = []
        url = f"{self._endpoint}/{id}/job_groups"
        resp = self.client.request(GET, url)
        for job_group in resp["data"]:
            _dict = {**job_group, "_resource": PyroJobGroupResource(self.client)}
            job_groups.append(PyroJobGroup.from_dict(_dict))

        return job_groups

    def list_ungrouped_jobs(self, id: str) -> list[PyroJob]:
        """
        # Retrieves ungrouped jobs in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project_id = "p_2VF7h.."
        jobs = pyro.projects.list_ungrouped_jobs(project_id)
        ```
        """
        url = f"{self._endpoint}/{id}/jobs"
        resp = self.client.request(GET, url)
        jobs = []
        for lite_job_data in resp["data"]:
            job_id = lite_job_data["id"]
            url = f"jobs/{job_id}"
            job_resp = self.client.request(GET, url)
            _dict = {**job_resp, "_resource": PyroJobResource(self.client)}
            jobs.append(PyroJob.from_dict(_dict))

        return jobs


@dataclass
class PyroProject:
    id: str
    name: str
    created_at: str
    is_active: str
    _resource: Optional[PyroProjectResource]

    @classmethod
    def from_dict(cls, d: dict) -> "PyroProject":
        return PyroProject(
            d["id"],
            d["name"],
            d["created_at"],
            d["is_active"],
            d["_resource"],
        )

    @require_resource
    def add_job(self, job_id: str):
        """
        # Add a job to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.create('test project')
        job_id = "j_r62X.."
        job = project.add_job(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.add_job(self.id, job_id)

    @require_resource
    def delete(self):
        """
        # Delete a project

        Deleting a project will also delete any jobs and data
        associated with it. Tread carefully.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my cringe project")
        project.delete()
        ```
        """
        assert self._resource is not None
        return self._resource.delete(self.id)

    @require_resource
    def duplicate_job(self, job_id: str):
        """
        # Duplicate a job in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.find_by_name("my project")
        job_id = "j_r62X.."
        duped_job = project.duplicate_job(job_id)
        ```
        """
        assert self._resource is not None
        return self._resource.duplicate_job(self.id, job_id)

    @require_resource
    def list_jobs(self):
        """
        # Retrieve all jobs in a project

        This function will return ALL jobs in a project,
        those that are directly associated with a project
        and those that are associated with a project
        through a job group.

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.filter("my project")
        jobs = project.list_jobs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_jobs(self.id)

    @require_resource
    def create_job(self, job: Union[PyroJob, dict]):
        """
        # Creates a new job in this project

        Creates a job and handles automatically adding it to a project.

        You can specify either a `PyroJob` or a `dict` as the `job` parameter.
        The system will automatically use the fields in this object to create
        an entirely new job in this project.

        When you specify a `PyroJob` a new job is created that is simply "modelled"
        after that job i.e. using a set of its properties.

        ## Args:
            id (str): project id
            job (Union[PyroJob | dict]): the properties to use when creating the job

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.get("p_2VF7h")
        new_job = project.create_job({"type": "fsim", "name": "my fsim job"})
        assert new_job.name == "my fsim job"
        ```
        """
        assert self._resource is not None
        return self._resource.create_job(self.id, job)

    @require_resource
    def add_job_group(self, job_group_id: str):
        """
        # Add job group to a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.get("p_2VF7h")
        job_group = project.add_job_group("jg_la043")
        ```
        """
        assert self._resource is not None
        return self._resource.add_job_group(self.id, job_group_id)

    @require_resource
    def list_job_groups(self):
        """
        # Retrieves job groups in a project

        ## Example
        ```python
        pyro = PyroDash(...)
        project = pyro.projects.get("p_2VF7h")
        job_groups = project.list_job_groups()
        ```
        """
        assert self._resource is not None
        return self._resource.list_job_groups(self.id)

    @require_resource
    def list_ungrouped_jobs(self):
        """
        # Retrieves ungrouped jobs in a project

        ## Example
        ```python
        jobs = project.list_ungrouped_jobs()
        ```
        """
        assert self._resource is not None
        return self._resource.list_ungrouped_jobs(self.id)
