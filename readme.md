# asynchronous-service-communication 

## Task to implement
![](./taskGivenToMe1.png)
![](./taskGivenToMe2.png)

# Brief overview of the solution

The solution is written in python3 (django). Main parts are
1. API controller: a `django` web service. For details please check the 
   file `asynchronous_service_communication/views.py`). It works as follows: 
   - Receives request
   - validates input 
   - save the request in the database
   - push message (the primary key of the row just savaed) in `redis` for the 
     `celery` worker 
   - immediately responds with an acknowledgement that request is received 
2. `Internal Authorization Service`: a `celery` worker with `redis` as 
   message queue. For details please check the file 
   `asynchronous_service_communication/tasks.py` . It works as follows:
   - It pops message (i.e. primary key) from the queue. 
   - Fetch the request row saved from database
   - It then checks `Access Control List 
     (ACL)` to make a decision.
   - Modify the existing request in the database with the decision
   - Send a callback to the client informing the decision
3. A job that is running after every `CRON_JOB_SLEEP_TIME_IN_SECONDS`  (`CRON_JOB_SLEEP_TIME_IN_SECONDS` may vary). For detaisl 
   please check the file `asynchronous_service_communication/management/commands/give_decision_after_timeout.py`
   - it fetches a list of requests that has both the characteristics 
     - created before `TIMEOUT_IN_SECONDS`  (`TIMEOUT_IN_SECONDS` may vary)
     - not got any decision from `Internal Authorization Service`
   - for each request of the above mentioned list
     - give each request decision as `unknown`
     - save the request in database
     - Send a callback to the client informing the decision

# Database used

`SQLite` database is used for this solution. It's built in django and no 
need of any extra installation.

For checking details about database and table please check the file 
`asynchronous_service_communication/models.py`.

# How to run it 

For running main program or test cases we need to do the following things:
1. Python3 installation
2. Redis installation
3. Dependency installation

## Python3 installation
The solution is written in python3. If we don't have python3 in our 
machine, we need to install it. For details we can check [python 3 download 
and 
installation](https://www.python.org/downloads/) 

## Redis installation
If redis is not installed, we need to install redis. Please follow [the 
link](https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/) for redis installation.

### verifying redis installation
Once Redis is running, we should be able to get back a `PONG` if you send a 
`ping` to `redis-cli` in terminal
```
$ redis-cli ping
PONG
```

## Dependency installation
1. We need go to the root folder of this project.
2. Then need to run `python3 -m pip install -r requirements.txt`

## How to run test case
1. Please go to the root folder of this project.
2. Then need to run in terminal `manage.py test`

If the tests passed, we should be able to see a output like this:
```
nafee.zahid@Mds-MacBook-Pro asynchronous-service-communication % ./manage.py test
Found 6 test(s).
System check identified no issues (0 silenced).
...Bad Request: /charge_point/session/
.Bad Request: /charge_point/session/
..
----------------------------------------------------------------------
Ran 6 tests in 0.058s

OK
```

If the test fails, we should be able to see a failure warning like this:
```
(.venv) nafee.zahid@Mds-MacBook-Pro asynchronous-service-communication % ./manage.py test
Found 6 test(s).
System check identified no issues (0 silenced).
...Bad Request: /charge_point/session/
FBad Request: /charge_point/session/
..
======================================================================
FAIL: test_get_request_should_post (asynchronous_service_communication.test_view.ViewTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/nafee.zahid/Desktop/rootForHardDisk/personal/Career/recruitmentsInDifferentCompanies/chargePoint/asynchronous-service-communication/asynchronous_service_communication/test_view.py", line 56, in test_get_request_should_post
    self.assertDictEqual(
AssertionError: {'sta[25 chars]'Invalid request method. request is GET. But should be POST.'} != {'sta[25 chars]'Invalid request method. request is GET. But should be POST. '}
- {'error': 'Invalid request method. request is GET. But should be POST.',
+ {'error': 'Invalid request method. request is GET. But should be POST. ',
?                                                                       +

   'status': 'failed'}

----------------------------------------------------------------------
Ran 6 tests in 0.060s

FAILED (failures=1)

```

# How to run the main program

## How to run the django webserver

Please go to root folder of this project.

Then need to run in terminal
```
service_name=webservice python3 manage.py runserver
```

It would start running the webserver. The webserver by default would listen to 
`http://127.0.0.1:8000/`. And we would be able to see the logs 
both in console and in the file named `webservice.log`. 

### How to hit the only public api endpoint

#### HTTP method
POST

#### Endpoint path
`/charge_point/session/`

So if the webserver is listening to  `http://127.0.0.1:8000/` the final path is `http://127.0.0.1:8000/charge_point/session/`

#### Request Parameters
The request body must be in JSON format and include the following parameters:

- Station Identifier: A UUID
- Driver Identifier: A string token of 20 to 80 characters in length. Allowed 
  characters include:
  - Uppercase letters ( A-Z )
  - Lowercase letters ( a-z )
  - Digits ( 0-9 )
  - Hyphen ( - ), period ( . ), underscore ( _ ), and tilde ( ~ ).
- Callback URL: A valid HTTP/HTTPS endpoint is provided by the client to 
    receive the final decision.

##### Sample request body
``` 
{
    "station_id": "123e4567-e89b-12d3-a456-426614174000",
    "driver_token": "validDriverToken1234567",
    "callback_url": "https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12"
}
```

For callback request you can give an url from any webiste providing free 
webhook like [webhook](https://webhook.site/)


##### Sameple response

If request is ok, then:
``` 
{
    "status": "accepted",
    "message": "Request is being processed asynchronously. The result will be sent to the provided callback URL."
}
```

If the request has some issues (for example station_id is not valid UUID), then:
```
{
    "status": "failed",
    "error": "station id is not a valid uuid"
} 
```




## How to run the celery i.e. Internal Authorization Service

Please go to the root folder of the project.

Then need to run in terminal:
```
service_name=celery celery -A asynchronous_service_communication worker 
--loglevel=info
```

It should start the celery and we are able to see the logs in console. 
Please note that once a decision is taken the decision in persisted in the 
database. And the decision is sent to the callback url.


## How to run the command / Cronjob

Please go to the root of the project.
Then in terminal run 

```
service_name=command TIMEOUT_IN_SECONDS=10 CRON_JOB_SLEEP_TIME_IN_SECONDS=30 python3 manage.py give_decision_after_timeout service_name=command python3 manage.py give_decision_after_timeout
```

You can give your preferred value for the `TIMEOUT_IN_SECONDS` and 
`CRON_JOB_SLEEP_TIME_IN_SECONDS`.

It should start our cron job and start printing the logs in console and in 
the file 'command.log'.

## Check the database

For checking details about database please inspect the file named `asynchronous_service_communication/models.py`

Please go to the root folder of the project.

Then let's run following command in terminal.
```
python3 manage.py shell
```

Then the django shell would open like this.
```
nafee.zahid@Mds-MacBook-Pro asynchronous-service-communication % python3 manage.py shell
Python 3.9.18 (main, Oct 31 2023, 12:06:58) 
[Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
```


There we need to import our database model with this command 
```
from asynchronous_service_communication.models import DecisionInstance
```

Then we can search how many rows are there in our database table with this query
```
len(DecisionInstance.objects.all())
```

Also we can fetch our rows (sorted according to primary key desc) from the 
table with this command:

```
DecisionInstance.objects.order_by('-pk').all()[start:end] 
```

Please insert value for start and end here.

Here is an example database inspection:


```
(.venv) nafee.zahid@Mds-MacBook-Pro asynchronous-service-communication % python3 manage.py shell
Python 3.9.18 (main, Oct 31 2023, 12:06:58) 
[Clang 15.0.0 (clang-1500.0.40.1)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from asynchronous_service_communication.models import DecisionInstance
>>> len(DecisionInstance.objects.all())
20
>>> DecisionInstance.objects.order_by('-pk').all()[3:6]
<QuerySet [<DecisionInstance: 
primary key = 17, 
station_id = 123e4567-e89b-12d3-a456-426614174000, 
driver_token = validDriverToken1234567,  
created_at = 2025-06-10 07:55:08.363632+00:00, 
decision = DecisionTypes.ALLOWED, 
updated_at = 2025-06-10 08:19:23.313668+00:00, 
callback_url = https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12, 
decision_taken_by = DecisionTakenByTypes.INTERNAL_AUTHORIZATION_SERVICE, 

>, <DecisionInstance: 
primary key = 16, 
station_id = 123e4567-e89b-12d3-a456-426614174000, 
driver_token = validDriverToken1234567,  
created_at = 2025-06-10 07:54:15.158034+00:00, 
decision = DecisionTypes.ALLOWED, 
updated_at = 2025-06-10 08:19:23.313668+00:00, 
callback_url = https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12, 
decision_taken_by = DecisionTakenByTypes.INTERNAL_AUTHORIZATION_SERVICE, 

>, <DecisionInstance: 
primary key = 15, 
station_id = 123e4567-e89b-12d3-a456-426614174000, 
driver_token = validDriverToken1234567,  
created_at = 2025-06-10 07:47:05.989652+00:00, 
decision = DecisionTypes.ALLOWED, 
updated_at = 2025-06-10 08:19:23.307499+00:00, 
callback_url = https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12, 
decision_taken_by = DecisionTakenByTypes.INTERNAL_AUTHORIZATION_SERVICE, 

>]>
>>> exit()
(.venv) nafee.zahid@Mds-MacBook-Pro asynchronous-service-communication % 

```




