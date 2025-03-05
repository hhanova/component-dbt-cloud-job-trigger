  
=============  

# DBT Cloud Job Trigger

**Table of contents:**

[TOC]

Functionality Notes
===================  
This component triggers a dbt Cloud job and optionally saves job information at trigger time and after job completion.

It then saves the response from [dbt Cloud API](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Jobs/operation/triggerRun) into the `dbt_cloud_trigger` table.

If the "wait_for_result" parameter is set to `true`, the component waits for the job to complete for the maximum time defined by
`max_wait_time`. It then stores the result of the [getRunById](https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getRunById) API call into the `dbt_cloud_run` table and saves all available artifacts.

Prerequisites
=============  

**API key:** Required for authentication. Instuctions on how to obtain one can be found <a href='https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html'>here</a>.

Supported Endpoints
===================  

If additional endpoints are needed, please submit a request at [ideas.keboola.com](https://ideas.keboola.com/).

Configuration
=============  

### Extractor Configuration

- Account ID (account_id) - [REQ] Numeric ID of the account
- Job ID (job_id) - [REQ] Numeric ID of the job
- API key (#api_key) - [REQ] Required for authentication (API key string). Instructions on how to obtain one can be found <a href='https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html'>here</a>.
- Cause (cause) - [REQ] String identifier sent with the job trigger request.
- Wait for result (wait_for_result) - [REQ] Set to `true` if you want the component to wait until the job finishes before storing artifacts.
- Max wait time (max_wait_time) - [OPT] Maximum wait time for job completion. Used only when **Wait for result** is `true`.
- Don't store artifacts - [OPT] Select this option if you want the component to ignore artifacts.

### Sample Configuration

```json  
{
    "parameters": {
        "account_id": 949,
        "job_id": 121341,
        "#api_key": "SECRET_VALUE",
        "cause": "Job triggered from Keboola",
        "wait_for_result": true,
        "ignore_artifacts": false
    },
    "action": "run"
}  
```  

Output
======  


**Tables:**

`in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_trigger`

`in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_run`

**Artifacts:**

Saves all artifacts from https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getArtifactsByRunId into Keboola
Storage.

Development
====== 

If needed, update the local data folder path by replacing the `CUSTOM_FOLDER` placeholder in the `docker-compose.yml` file:

`volumes: - ./:/code - ./CUSTOM_FOLDER:/data`
  
Clone this repository, initialize the workspace, and run the component using the following commands:  
  
`docker-compose build`
`docker-compose run --rm dev`

  
Run the test suite and perform a lint check using this command:  
  
`docker-compose run --rm test`


Integration
=======

For details on deployment and integration with Keboola, refer to the [deployment section of the developer documentation](https://developers.keboola.com/extend/component/deployment/).
