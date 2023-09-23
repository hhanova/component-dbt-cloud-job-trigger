import backoff
import requests
import os
from pathlib import Path
import logging

from requests.exceptions import HTTPError
from keboola.component.exceptions import UserException


class DbtClient:

    def __init__(self, account_id,
                 job_id,
                 api_key
                 ):
        self.account_id = account_id
        self.job_id = job_id
        self.api_key = api_key

        self.auth_headers = {'Authorization': f"Token {api_key}"}

    def fetch_artifact(self, job_run_id: int, artifact: str) -> None:
        """
        Gets available artifacts and stores them in temp folder.
        Args:
            artifact: Path to artifact
            job_run_id: Job run ID
        """
        res = requests.get(
            url=f"https://cloud.getdbt.com/api/v2/accounts/"
                f"{self.account_id}/runs/{job_run_id}/artifacts/{artifact}",
            headers=self.auth_headers
        )
        if res.status_code == 200:
            self.store_artifact(artifact, res.text)
            logging.info(f"Stored artifact: {artifact}")
        else:
            logging.warning(f"Cannot save {artifact}: {res.text}")

    @staticmethod
    def store_artifact(artifact: str, file: str) -> None:
        """
        Stores file in data/temp folder
        Args:
            artifact: filename
            file: string content to be stored
        """
        cwd = Path(os.getcwd())
        root_dir = cwd.parent.absolute()
        temp_dir = os.path.join(root_dir, "data", "artifacts", "out", "current")

        full_path = Path(os.path.join(temp_dir, artifact))
        parent_dir = full_path.parent.absolute()
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        with open(full_path, "w") as f:
            f.write(file)

    def trigger_job(self, cause: str) -> dict:
        """
        Triggers the dbt job.
        Returns dictionary with data field from response.

        Args:
            cause: String identifier which will be sent along with job trigger request.
        """
        res = requests.post(
            url=f"https://cloud.getdbt.com/api/v2/accounts/{self.account_id}/jobs/{self.job_id}/run/",
            headers=self.auth_headers,
            json={
                # Optionally pass a description that can be viewed within the dbt Cloud API.
                # See the API docs for additional parameters that can be passed in,
                # including `schema_override`
                'cause': cause,
            }
        )

        try:
            res.raise_for_status()
        except HTTPError:
            if res.json()["status"]["user_message"] == "Invalid token.":
                raise UserException("""Invalid API key has been set, job could not be triggered. Make sure your API
                key is valid and re-enter it into the component configuration.""")
            raise UserException(f"Encountered Error when triggering job: {res.text}")

        response_payload = res.json()
        return response_payload['data']

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3, factor=2)
    def get_job_run_status(self, job_run_id: int, get_steps=False) -> dict:
        res = requests.get(
            url=f"https://cloud.getdbt.com/api/v2/accounts/{self.account_id}/runs/{job_run_id}/",
            headers=self.auth_headers,
            params='include_related=["run_steps", "job"]' if get_steps else ""
        )

        try:
            res.raise_for_status()
        except HTTPError:
            raise UserException(f"Encountered Error when getting job status: {res.text}")

        return res.json()

    @backoff.on_exception(backoff.expo, HTTPError, max_tries=3, factor=2)
    def list_available_artifacts(self, job_run_id: int) -> list:
        res = requests.get(
            url=f"https://cloud.getdbt.com/api/v2/accounts/{self.account_id}/runs/{job_run_id}/artifacts/",
            headers={'Authorization': f"Token {self.api_key}"},
        )

        try:
            res.raise_for_status()
        except HTTPError:
            raise UserException(f"Encountered Error when triggering job: {res.text}")

        response_payload = res.json()
        return response_payload["data"]
