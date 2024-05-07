from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.contrib.auth.models import Group, User
from django.views.decorators.http import require_GET
from django.views import View
import json


class GroupUserViews(View):
    def __get_group(self, group_id: int) -> Group:
        return Group.objects.get(id=group_id)

    def __get_user(self, user_id: int) -> User:
        return User.objects.get(id=user_id)

    def get(self, _, group_id):
        """
        Get all users within the group
        """
        try:
            group = self.__get_group(group_id)
            users = group.user_set.all().values('id', 'username')
            return JsonResponse(list(users), safe=False)
        except Group.DoesNotExist:
            return HttpResponseBadRequest('Invalid Group Id')

    def post(self, request, group_id):
        """
        Add user into a group
        """
        try:
            group = self.__get_group(group_id)
            body = json.loads(request.body.decode('utf-8'))
            if 'user_id' not in body:
                raise ValueError('Missing Request body: user_id')
            user = self.__get_user(body['user_id'])
            group.user_set.add(user)
            return HttpResponse()
        except Group.DoesNotExist:
            return HttpResponseBadRequest('Invalid Group Id')
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid User Id')
