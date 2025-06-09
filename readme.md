# asynchronous-service-communication 

## Task to implement
![](./taskGivenToMe1.png)
![](./taskGivenToMe2.png)


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