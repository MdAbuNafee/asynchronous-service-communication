# asynchronous-service-communication 

service_name=webservice/celery/command

celery run:
celery -A asynchronous_service_communication worker --loglevel=info


webhook link to receive the callback:
https://webhook.site/a02530e4-62e6-433b-ae31-d1392e823f12


python3 manage.py runserver


python3 manage.py give_decision_after_timeout