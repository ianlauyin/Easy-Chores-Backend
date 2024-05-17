import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse, HttpResponseNotFound
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from ..models import User


class UserGroupViews(View):
    def get(self, _, user_id):
        """
        Get Groups of a user
        """
        try:
            user = User.objects.get(id=user_id)
            groups = user.groups.all().values()
            return JsonResponse(list(groups), safe=False)
        except User.DoesNotExist:
            return HttpResponseNotFound('Invalid UserId')
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')


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
