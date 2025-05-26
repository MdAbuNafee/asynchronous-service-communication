from django.urls import path
from driver import views

urlpatterns = [
    path('session', views.session, name='session')
]
