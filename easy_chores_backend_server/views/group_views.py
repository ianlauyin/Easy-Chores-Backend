from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse, HttpResponseServerError, HttpResponseNotFound, HttpRequest
from django.contrib.auth.models import Group
from ..models import User
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.query import QuerySet
from django.views.decorators.http import require_GET, require_POST
from django.views import View
from django.db import transaction
from .auth_views import verify_token
from django.utils.decorators import method_decorator
import json


@method_decorator(verify_token, name='dispatch')
class GroupUserViews(View):

    def get(self, _, group_id: int):
        """
        Get all users within the group
        """
        try:
            group = Group.objects.get(id=group_id)
            users = group.custom_user_set.all().values('id', 'email', 'username')
            return JsonResponse(list(users), safe=False)
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def post(self, _, group_id: int, user_email: str):
        """
        Add user into a group
        """
        try:
            group = Group.objects.get(id=group_id)
            user = User.objects.get(email=user_email)
            if user in group.custom_user_set.all():
                raise ValueError(
                    f'User Id ({user_email}) already in Group Id ({group_id})')
            group.custom_user_set.add(user)
            return HttpResponse(status=204)
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except User.DoesNotExist:
            return HttpResponseNotFound('Invalid User Id')
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def delete(self, _, group_id: int, user_email: str):
        """
        remove user from a group
        """
        try:
            group = Group.objects.get(id=group_id)
            user = User.objects.get(email=user_email)
            if user not in group.custom_user_set.all():
                raise ValueError(
                    f'User Id ({user_email}) is not in Group Id ({group_id})')
            group.custom_user_set.remove(user)
            return HttpResponse(status=204)
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except User.DoesNotExist:
            return HttpResponseNotFound('Invalid User Id')
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
        except:
            return HttpResponseServerError('Error is occured. Please try again later')


@require_POST
@verify_token
def create_group(request: HttpRequest):
    try:
        with transaction.atomic():
            data: dict[str] = json.loads(request.body)
            if 'user_id' not in data:
                raise ValueError('user_id')
            if 'name' not in data:
                raise ValueError('name')
            new_group = Group.objects.create(name=data['name'])
            user = User.objects.get(id=data['user_id'])
            new_group.custom_user_set.add(user)
            return JsonResponse({"group_id": new_group.id})
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Required JSON body data")
    except User.DoesNotExist:
        return HttpResponseNotFound("Invalid user_id")
    except ValueError as e:
        return HttpResponseBadRequest(f'Missing Required body: {e}')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


@require_GET
@verify_token
def get_grocery_list(_, group_id: int):
    try:
        group = Group.objects.get(id=group_id)
        groceries: QuerySet = group.groceries.all().values(
            'id', 'name', 'creator__username', 'quantity', 'created_at')

        return JsonResponse(list(groceries), safe=False)
    except Group.DoesNotExist:
        return HttpResponseNotFound('Invalid Group Id')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


@require_GET
@verify_token
def get_chore_list(_, group_id: int):
    try:
        group = Group.objects.get(id=group_id)
        chores: QuerySet = group.chores.filter(completed_date=None).values('id', 'title', 'created_at').annotate(
            assigned_users=ArrayAgg('assigned_users__username'))
        return JsonResponse(list(chores), safe=False)
    except Group.DoesNotExist:
        return HttpResponseNotFound('Invalid Group Id')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')
