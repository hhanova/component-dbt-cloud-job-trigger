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
 "parameters": { "account_id": 949, "job_id": 121341, "#api_key": "SECRET_VALUE", "cause": "Job triggered from Keboola", "wait_for_result": true }, "action": "run"}  
```  