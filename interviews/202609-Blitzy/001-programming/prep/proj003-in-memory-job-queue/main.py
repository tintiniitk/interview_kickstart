"""
In-memory job queue that accepts jobs and reports their status.

Requirements:
1. POST /jobs {"description": "xyz", "duration_seconds": <num>} => Creates a new job item in memory and returns {"id": <unique_id>, "description": "...", "start_time": time_in_utc, "end_time": time_in_utc, "status": "<status_string>" } ::: Service also stores an id, status, start_time, end_time per job internally.
2. GET /jobs

"""

from collections import deque
from datetime import UTC, datetime, timedelta
from enum import Enum

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class JobStatus(str, Enum):
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    DONE = "DONE"


class Job(BaseModel):
    id: int
    description: str
    queued_time: datetime
    start_time: datetime
    end_time: datetime
    status: JobStatus = JobStatus.QUEUED
"""  """

class JobCreationRequest(BaseModel):
    description: str
    duration_seconds: int


app = FastAPI(title="In-memory job queue")

# state
next_job_id = 1

# DB
jobs_db: dict[int, Job] = {}
job_queue = deque([])

# configuration
AUTO_REMOVE_DONE_JOBS: bool = True


@app.post(path="/jobs", response_model=Job, status_code=201)
def create_job(payload: JobCreationRequest) -> Job:
    def get_next_job_id():
        global next_job_id
        ret = next_job_id
        next_job_id += 1
        return ret

    # handle bad inputs.
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=r"no input data passed, expected data in format: {{ \"description\": \"job description e.g. process object x>\", \"duration_seconds\": num }}",
        )
    if not payload.description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=r"description is either missing or is empty in input data",
        )
    if payload.duration_seconds <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=r"duration_seconds is <= 0 in input data",
        )

    # create a new job with the given details and right after (or latest now, whichever is later) the last scheduled job.
    now = datetime.now(tz=UTC)
    start = now
    if job_queue:
        last_schedule_job = job_queue[-1]
        if last_schedule_job in jobs_db and jobs_db[last_schedule_job].end_time > now:
            start = jobs_db[last_schedule_job].end_time
    end = start + timedelta(seconds=payload.duration_seconds)
    job = Job(
        id=get_next_job_id(),
        description=payload.description,
        queued_time=now,
        start_time=start,
        end_time=end,
    )

    # register this new job
    jobs_db[job.id] = job
    job_queue.append(job.id)
    return job


def update_statuses():
    cur_time = datetime.now(tz=UTC)
    index = 0
    while index < len(job_queue):
        job_id = job_queue[index]
        index += 1
        job = jobs_db[job_id]
        if cur_time < job.start_time:
            job.status = JobStatus.QUEUED
        elif job.end_time > cur_time >= job.start_time:
            job.status = JobStatus.IN_PROGRESS
        else:
            job.status = JobStatus.DONE
            if AUTO_REMOVE_DONE_JOBS:
                job_queue.popleft()
                del jobs_db[job_id]
                index -= 1


@app.get(path="/jobs", response_model=list[Job])
def get_jobs() -> list[Job]:
    update_statuses()
    return list(jobs_db.values())


@app.get(path="/jobs/{id}", response_model=Job)
def get_job(id: int) -> Job:
    if id not in jobs_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=rf"no item found id={id}",
        )
    update_statuses()
    return jobs_db[id]


@app.get(path="/")
def get() -> dict[str, str]:
    return {"status": "Up and running"}


@app.delete(path="/jobs")
def delete_all_jobs():
    global jobs_db
    global job_queue
    jobs_db = {}
    job_queue = []
    return "All jobs removed from queue."
