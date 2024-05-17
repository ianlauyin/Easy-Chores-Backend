from django.views import View
from ..models import Chore, User
from django.contrib.auth.models import Group
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponse, HttpRequest
from django.forms import model_to_dict
import json
import datetime


class ChoreViews(View):
    def get(self, _, chore_id: int):
        """
        Get Chore Detail with assigned users name and id
        """
        try:
            chore = Chore.objects.get(id=chore_id)
            chore_data = model_to_dict(chore)
            chore_data['assigned_users'] = [
                {'id': assigned_user.id, 'username': assigned_user.username} for assigned_user in chore_data['assigned_users']]
            return JsonResponse(chore_data, safe=False)
        except Chore.DoesNotExist:
            return HttpResponseNotFound('Invalid chore id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def post(self, request: HttpRequest):
        """
        Create Chore item
        """
        try:
            data: dict[str] = json.loads(request.body)
            check_keys = ['group_id', 'title']
            missing_keys = [key for key in check_keys if key not in data]
            if len(missing_keys) > 0:
                raise ValueError(', '.join(missing_keys))
            group = Group.objects.get(id=data['group_id'])
            new_chore_data = {'title': data['title']}
            if 'detail' in data:
                new_chore_data['detail'] = data['detail']
            new_chore = Chore.objects.create(group=group, **new_chore_data)
            return JsonResponse({'id': new_chore.id}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except ValueError as e:
            return HttpResponseBadRequest(f'Missing Required body:{e}')
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def put(self, request: HttpRequest, chore_id: int):
        """
        Update Chore Detail
        """
        try:
            chore = Chore.objects.get(id=chore_id)
            data: dict[str] = json.loads(request.body)
            editable_str_list = ['title', 'detail']
            not_changed = True
            for key in editable_str_list:
                if key in data:
                    if not isinstance(data[key], str):
                        raise TypeError(
                            f'Required string type of key: {key}')
                    not_changed = False
                    setattr(chore, key, data[key])
            if 'completed_date' in data:
                not_changed = False
                completed_date = datetime.datetime.strptime(
                    data['completed_date'], '%Y-%m-%d').date()
                setattr(chore, 'completed_date', completed_date)
            if not_changed:
                raise ValueError(
                    'Must have at least one key: title, detail, completed_date')
            chore.save()
            return HttpResponse(status=204)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except (ValueError, TypeError)as e:
            return HttpResponseBadRequest(str(e))
        except Chore.DoesNotExist:
            return HttpResponseNotFound('Invalid chore Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def delete(self, _, chore_id: int):
        """
        Delete Chore Item
        """
        try:
            chore = Chore.objects.get(id=chore_id)
            chore.delete()
            return HttpResponse(status=204)
        except Chore.DoesNotExist:
            return HttpResponseNotFound('Invalid chore Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')


@require_http_methods(['PUT'])
def rearrange_chores_assigned_users(request: HttpRequest, chore_id: int):
    try:
        chore = Chore.objects.get(id=chore_id)
        data: dict[str] = json.loads(request.body)
        if 'user_ids' not in data:
            raise ValueError('Require key: user_ids:list[int]')
        if not isinstance(data['user_ids'], list):
            raise TypeError('Wrong Type for user_ids, need list')
        for user_id in data['user_ids']:
            if not isinstance(user_id, int):
                raise TypeError('Wrong Type of user_id, need int')
        new_assigned_users = User.objects.filter(id__in=data['user_ids'])
        chore.assigned_users.set(new_assigned_users)
        return HttpResponse(status=204)
    except (ValueError, TypeError) as e:
        return HttpResponseBadRequest(str(e))
    except Chore.DoesNotExist:
        return HttpResponseNotFound('Invalid chore id')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')
