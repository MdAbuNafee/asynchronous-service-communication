# asynchronous-service-communication 

## Task to implement
![](./taskGivenToMe1.png)
![](./taskGivenToMe2.png)

# Brief overview of the solution

The solution is written in python3 (django). Main parts are
1. API controller: a django web service:
   - Receives request
   - validates input 
   - save the request in the database
   - push message (the primary key of the row just savaed) in `redis` for the 
     `celery` worker 
   - immediately responds with an acknowledgement that request is received 
2. `Internal Authorization Service`: a `celery` worker with `redis` as 
   message queue
   - It pops message (i.e. primary key) from the queue. 
   - Fetch the request row saved from database
   - It then checks `Access Control List 
     (ACL)` to make a decision.
   - Modify the existing request in the database with the decision
   - Send a callback to the client informing the decision
3. A job that is running after every `x` seconds (`x` may vary)
   - it fetches a list of requests that has both the characteristics 
     - created before `y` seconds (`y` may vary)
     - not got any decision from `Internal Authorization Service`
   - for each request of the above mentioned list
     - give each request decision as `unknown`
     - save the request in database
     - Send a callback to the client informing the decision


# How to run it 

service_name=webservice/celery/command

celery run:
celery -A asynchronous_service_communication worker --loglevel=info


webhook link to receive the callback:
https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12


python3 manage.py runserver


python3 manage.py give_decision_after_timeout


Check how many DecisionInstance are in DB:
len(DecisionInstance.objects.all())

for checking database
python manage.py shell

for importing DecisionInstance
from asynchronous_service_communication.models import DecisionInstance

Fetch DecisionInstance sorted by desc primary key 
DecisionInstance.objects.order_by('-pk').all()[start:end] [start, start+1, ..
..., end-2, end-1]
example: DecisionInstance.objects.order_by('-pk').all()[1:2]




Before running test.
need to run this in terminal.
export DJANGO_SETTINGS_MODULE=asynchronous_service_communication.settings

Then run test suite: 
./manage.py test