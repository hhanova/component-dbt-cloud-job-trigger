"""
Template Component main class.
inspired by:
https://discourse.getdbt.com/t/triggering-a-dbt-cloud-job-in-your-automated-workflow-with-python/2573
"""
import csv
import logging
import os
import time
import enum
from requests.exceptions import HTTPError
from pathlib import Path

from keboola.component.base import ComponentBase
from mapping import assign_status_data
from client import DbtClient

from keboola.component.exceptions import UserException

# configuration variables
ACCOUNT_ID = "account_id"
JOB_ID = "job_id"
API_KEY = "#api_key"
CAUSE = "cause"
WAIT_FOR_RESULT = "wait_for_result"
MAX_WAIT_TIME = "max_wait_time"

# list of mandatory parameters => if some is missing,
# component will fail with readable message on initialization.
REQUIRED_PARAMETERS = [ACCOUNT_ID, JOB_ID, API_KEY, CAUSE, WAIT_FOR_RESULT]
REQUIRED_IMAGE_PARS = []


# These are documented on the dbt Cloud API docs
class DbtJobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


class Component(ComponentBase):
    """
        Extends base class for general Python components. Initializes the CommonInterface
        and performs configuration validation.

        For easier debugging the data folder is picked up by default from `../data` path,
        relative to working directory.

        If `debug` parameter is present in the `config.json`, the default logger is set to verbose DEBUG mode.
    """

    def __init__(self):
        super().__init__()

        self.validate_configuration_parameters(REQUIRED_PARAMETERS)
        params = self.configuration.parameters
        self.output_bucket = self.get_bucket_name()

        self.account_id = params.get(ACCOUNT_ID)
        self.job_id = params.get(JOB_ID)
        self.api_key = params.get(API_KEY)
        if self.api_key == "":
            raise UserException("API key cannot be empty.")
        self.cause = params.get(CAUSE)
        if wait_for_result := params.get(WAIT_FOR_RESULT):
            try:
                self.max_wait_time = params.get(MAX_WAIT_TIME * 60)
            except TypeError:
                self.max_wait_time = None
        self.wait_for_result = wait_for_result

        cwd = Path(os.getcwd())
        root_dir = cwd.parent.absolute()
        self.artifacts_dir = os.path.join(root_dir, "data", "artifacts", "out", "current")
        self.data_dir = (os.path.join(root_dir, "data"))

    def run(self):
        """
        Main execution code
        """

        client = DbtClient(account_id=self.account_id,
                           job_id=self.job_id,
                           api_key=self.api_key
                           )

        job_run_data = client.trigger_job(cause=self.cause)
        job_run_id = job_run_data['id']
        job_run_url = job_run_data['href']
        logging.warning(f'Run triggered: {job_run_url}')

        self.save_dict_to_csv(job_run_data, "dbt_cloud_trigger")

        if self.wait_for_result:
            start_time = time.time()
            while True:
                time.sleep(30)

                try:
                    data = self._get_job_run_status(client, job_run_id, get_steps=True)['data']
                except HTTPError as e:
                    raise UserException(f"Encountered Error when getting job status: {e}") from e

                status = data['status']
                logging.info(f"Job status = {DbtJobRunStatus(status).name}")

                if status == DbtJobRunStatus.SUCCESS:
                    for artifact in self._list_available_artifacts(client, job_run_id):
                        client.fetch_artifact(job_run_id, artifact)
                    break
                elif status == DbtJobRunStatus.ERROR:
                    raise UserException(f"Job with ID {job_run_id} has been stopped."
                                        f"Run steps: {data['run_steps']}")
                elif status == DbtJobRunStatus.CANCELLED:
                    raise UserException(f"Job with ID {job_run_id} has been canceled by user.")

                # Stop waiting if runtime is greater than MAX_WAIT_TIME (minutes)
                if self.max_wait_time:
                    if (time.time() - start_time) < self.max_wait_time:
                        raise UserException(f"Max wait time reached for Job with ID {job_run_id} - Exiting.")

        status_data = self._get_job_run_status(client, job_run_id)
        run_data = assign_status_data(status_data)
        self.save_dict_to_csv(run_data, "dbt_cloud_run")

        logging.info("Component finished successfully.")

    def get_bucket_name(self) -> str:
        config_id = self.environment_variables.config_id
        if not config_id:
            config_id = "000000000"
        bucket_name = f"in.c-dbt-cloud-job-trigger-{config_id}"
        return bucket_name

    def save_dict_to_csv(self, input_dct, filename):
        table = self.create_out_table_definition(name=filename, incremental=True,
                                                 destination=f"{self.output_bucket}.{filename}")
        with open(table.full_path, mode="w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, input_dct.keys())
            w.writeheader()
            w.writerow(input_dct)
        self.write_manifest(table)

    @staticmethod
    def _list_available_artifacts(client, job_run_id) -> list:
        try:
            return client.list_available_artifacts(job_run_id)
        except HTTPError as e:
            raise UserException(f"Encountered Error when getting job artifacts: {e}") from e

    @staticmethod
    def _get_job_run_status(client, job_run_id: int, get_steps=False) -> dict:
        try:
            return client.get_job_run_status(job_run_id, get_steps)
        except HTTPError as e:
            raise UserException(f"Encountered Error when getting job status: {e}") from e


"""
        Main entrypoint
"""
if __name__ == "__main__":
    try:
        comp = Component()
        # this triggers the run method by default and is controlled by the configuration.action parameter
        comp.execute_action()
    except UserException as exc:
        logging.exception(exc)
        exit(1)
    except Exception as exc:
        logging.exception(exc)
        exit(2)
