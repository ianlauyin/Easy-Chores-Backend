from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import Group
from django.views.decorators.http import require_GET
from django.views import View


class GroupUserViews(View):
    def get(self, _, group_id):
        try:
            group = Group.objects.get(id=group_id)
            users = group.user_set.all().values('id', 'username')
            return JsonResponse(list(users), safe=False)
        except Group.DoesNotExist:
            return HttpResponseBadRequest('Invalid Group Id')
