  
=============  

# DBT Cloud Job Trigger

**Table of contents:**

[TOC]

Functionality notes
===================  
Triggers dbt Cloud job. Optionally, saves job info at trigger time and after the job is done.

Next, saves response from https://docs.getdbt.com/dbt-cloud/api-v2#tag/Jobs/operation/triggerRun into table *
*dbt_cloud_trigger**.

If the parameter "wait_for_result" is set to true, waits for the job to complete for the maximum time set via
parameter "max_wait_time" then stores result of https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getRunById
into table **dbt_cloud_run** and stores all available artifacts.

Prerequisites
=============  

**API key:** API Key string, How to get one is
explained <a href='https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html'>here</a>"

Supported endpoints
===================  

If you need more endpoints, please submit your request to  
[ideas.keboola.com](https://ideas.keboola.com/)

Configuration
=============  

##extractor configuration

- Account ID (account_id) - [REQ] Numeric ID of the account
- Job ID (job_id) - [REQ] Numeric ID of the job
- API Key (#api_key) - [REQ] API Key string, How to get one is
  explained <a href='https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html'>here</a>
- Cause (cause) - [REQ] String identifier which will be sent along with job trigger request.
- Wait for result (wait_for_result) - [REQ] Set to true if you want the component to wait until defined job finishes and
  then store artifacts.
- Max wait time (max_wait_time) - [OPT] Max time to wait. Used only when parameter Wait for result is set to true.
- Don't store artifacts - [OPT] Select this if you want the component to ignore artifacts.

Sample Configuration
=============  

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

in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_trigger

in.c-dbt-cloud-job-trigger-{config_id}.dbt_cloud_run

**Artifacts:**

Saves all artifacts from https://docs.getdbt.com/dbt-cloud/api-v2#tag/Runs/operation/getArtifactsByRunId into Keboola
storage.

Development
====== 

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to your custom path in  
the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
 volumes: - ./:/code - ./CUSTOM_FOLDER:/data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
Clone this repository, init the workspace and run the component with following command:  
  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

docker-compose build  
docker-compose run --rm dev

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
Run the test suite and lint check using this command:  
  
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  

docker-compose run --rm test

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  
  
Integration  
===========  
  
For information about deployment and integration with KBC, please refer to the  
[deployment section of developers documentation](https://developers.keboola.com/extend/component/deployment/)