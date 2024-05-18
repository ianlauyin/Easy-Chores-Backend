
from django.http import HttpResponseServerError, JsonResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth.models import Group
from ..models import User
from ..views.auth_views import verify_token
from django.utils.decorators import method_decorator


@method_decorator(verify_token, name='dispatch')
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
