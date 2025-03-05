Triggers a dbt Cloud job and optionally saves job information at trigger time and after the job is completed.  

Then, it saves the response from the [triggerRun API](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Jobs/operation/triggerRun) into the `dbt_cloud_trigger` table.

If the "wait_for_result" parameter is set to `true`, the component waits for the job to complete for the maximum duration defined by `max_wait_time`. Once finished, it stores the result of the [getRunById API](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getRunById) into the `dbt_cloud_run` table and saves all available artifacts.
