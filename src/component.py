"""
Template Component main class.
inspired by:
https://discourse.getdbt.com/t/triggering-a-dbt-cloud-job-in-your-automated-workflow-with-python/2573
"""
import csv
import logging
from datetime import datetime
import time

from keboola.component.base import ComponentBase
from helper import DbtJobRunStatus
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

        self.account_id = params.get(ACCOUNT_ID)
        self.job_id = params.get(JOB_ID)
        self.api_key = params.get(API_KEY)
        self.cause = params.get(CAUSE)
        if wait_for_result := params.get(WAIT_FOR_RESULT) is True:
            try:
                self.max_wait_time = params.get(MAX_WAIT_TIME * 60)
            except TypeError:
                self.max_wait_time = None
        self.wait_for_result = wait_for_result

    def run(self):
        """
        Main execution code
        """

        client = DbtClient(account_id=self.account_id,
                           job_id=self.job_id,
                           api_key=self.api_key
                           )

        job_run_id = client.trigger_job(cause=self.cause)
        logging.info(f"Triggered Job Run ID: {job_run_id}")

        if self.wait_for_result:
            start_time = time.time()
            while True:
                time.sleep(5)

                status = client.get_job_run_status(job_run_id)
                logging.info(f"Job status = {DbtJobRunStatus(status).name}")

                if status == DbtJobRunStatus.SUCCESS:
                    client.get_artifacts(job_run_id)
                    break
                elif status == DbtJobRunStatus.ERROR or status == DbtJobRunStatus.CANCELLED:
                    raise UserException(f"Job with ID {job_run_id} has been stopped.")

                # Stop waiting if runtime is greater than MAX_WAIT_TIME (minutes)
                if self.max_wait_time:
                    if (time.time() - start_time) < self.max_wait_time:
                        raise UserException(f"Max wait time reached for Job with ID {job_run_id} - Exiting.")

        table = self.create_out_table_definition("output.csv", incremental=True, primary_key=["job_run_id", "ts"])

        # DO whatever and save into out_table_path
        with open(table.full_path, mode="wt", encoding="utf-8", newline="") as out_file:
            writer = csv.DictWriter(out_file, fieldnames=["job_run_id", "ts"])
            writer.writeheader()
            writer.writerow({
                "job_run_id": job_run_id,
                "ts": datetime.now().isoformat()
            })

        self.write_manifest(table)


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
