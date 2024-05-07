import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views import View
from django.core.exceptions import ValidationError


class UserViews(View):
    def post(self, request):
        """
        Create user data(Not Completed, need to integrate with apple sign)
        """
        try:
            data = json.loads(request.body.decode('utf-8'))
            if 'email' not in data:
                raise ValidationError('Missing required data: email')
            return HttpResponse()
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Invalid data')
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))


def UserLoginView(request):
    """
    Should be  integrate with apple sign
    """
    return
