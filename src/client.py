import requests
import json
import os
from pathlib import Path
import logging

from requests.exceptions import HTTPError
from keboola.component.exceptions import UserException


ARTIFACTS = ["manifest.json", "catalog.json", "run_results.json"]


def store_artifact(artifact: str, file: dict) -> None:
    """
    Stores file in data/out/artifacts folder
    Args:
        artifact: filename
        file: Dictionary with json content to be stored
    """
    cwd = Path(os.getcwd())
    root_dir = cwd.parent.absolute()
    artifacts_dir = (os.path.join(root_dir, "data", "out", "artifacts"))

    if not os.path.exists(artifacts_dir):
        logging.info("Creating artifacts directory.")
        os.makedirs(artifacts_dir)

    full_path = os.path.join(artifacts_dir, artifact)

    with open(full_path, "w") as f:
        json.dump(file, f)


class DbtClient:

    def __init__(self, account_id,
                 job_id,
                 api_key
                 ):
        self.account_id = account_id
        self.job_id = job_id
        self.api_key = api_key

        self.auth_headers = {'Authorization': f"Token {api_key}"}

    def get_artifacts(self, job_run_id: int) -> None:
        """
        Gets available artifacts and stores them in artifacts folder.
        Args:
            job_run_id: Job run ID
        """
        for artifact in ARTIFACTS:
            res = requests.get(
                url=f"https://cloud.getdbt.com/api/v2/accounts/{self.account_id}/runs/{job_run_id}/artifacts/{artifact}",
                headers=self.auth_headers
            )
            if res.status_code == 200:
                store_artifact(artifact, res.json())
            else:
                logging.warning(f"Cannot save {artifact}: {res.text}")

    def trigger_job(self, cause: str) -> int:
        """
        Triggers
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
            raise UserException(f"Encountered Error when triggering job: {res.text}")

        response_payload = res.json()
        return response_payload['data']['id']

    def get_job_run_status(self, job_run_id: int) -> int:
        """
        Fetches Job run status code.
        Args:
            job_run_id: Job run ID
        """
        res = requests.get(
            url=f"https://cloud.getdbt.com/api/v2/accounts/{self.account_id}/runs/{job_run_id}/",
            headers=self.auth_headers,
        )

        res.raise_for_status()
        response_payload = res.json()
        return response_payload['data']['status']
