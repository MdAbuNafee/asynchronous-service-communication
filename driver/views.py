from django.shortcuts import render
from django.views import View


# Create your views here.

import json

class SessionView(View):
    def post(self, request):
        post_data = json.loads(request.body.decode('utf-8'))
        return render(request, 'session.html')
