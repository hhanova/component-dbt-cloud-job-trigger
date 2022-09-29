Triggers dbt Cloud job. Optionally, saves job info at trigger time and after the job is done.  

Next, saves response from https://docs.getdbt.com/dbt-cloud/api-v2#tag/Jobs/operation/triggerRun into table **dbt_cloud_trigger**.

If the parameter "wait_for_result" is set to true, waits for the job to complete for the maximum time set via parameter "max_wait_time" then stores result of https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getRunById into table **dbt_cloud_run** and stores all available artifacts.
