import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
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
        except:
            return HttpResponseServerError('Error is occured. Please try again later')
