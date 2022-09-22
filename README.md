
=============

dbt job trigger

dbt Job trigger

Triggers dbt Cloud job. Optionally, saves job info at trigger time and after the job is done.

**Table of contents:**

[TOC]

Functionality notes
===================

Prerequisites
=============

Get the API token, register application, etc.


Supported endpoints
===================

If you need more endpoints, please submit your request to
[ideas.keboola.com](https://ideas.keboola.com/)

Configuration
=============

##extractor configuration
 - Account ID (account_id) - [REQ] Numeric ID of the account
 - Job ID (job_id) - [REQ] Numeric ID of the job
 - API Key (#api_key) - [REQ] API Key string, How to get one is explained <a href='https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html'>here</a>
 - Cause (cause) - [REQ] String identifier which will be sent along with job trigger request.
 - Wait for result (wait_for_result) - [REQ] Set to true if you want the component to wait until defined job finishes and then store artifacts.
 - Max wait time (max_wait_time) - [OPT] Max time to wait. Used only when parameter Wait for result is set to true.




Sample Configuration
=============
```json
{
    "parameters": {
        "account_id": 949,
        "job_id": 121341,
        "#api_key": "SECRET_VALUE",
        "cause": "Job triggered from Keboola",
        "wait_for_result": true
    },
    "action": "run"
}
```

Output
======

List of tables, foreign keys, schema.

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to your custom path in
the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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