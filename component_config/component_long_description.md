Requirements:

 - API key
 - Account ID
 - Job ID

### Output

Tables (data is going to be imported incrementally):  
 - in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_trigger - response from [api-v2#tag/Jobs/operation/triggerRun](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Jobs/operation/triggerRun)
 - in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_run - response from [api-v2#tag/Runs/operation/getRunById](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getRunById)

Artifacts:  

Saves all artifacts from https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getArtifactsByRunId into Keboola storage.

