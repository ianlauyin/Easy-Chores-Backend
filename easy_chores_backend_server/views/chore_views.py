from django.views import View
from ..models import Chore
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError, HttpResponse
from django.forms import model_to_dict
import json
import datetime


class ChoreViews(View):
    def get(self, _, chore_id):
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
            return HttpResponseBadRequest('Invalid chore id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def post(self, request):
        """
        Create Chore item
        """
        try:
            data = json.loads(request.body)
            check_keys = ['group_id', 'title']
            missing_keys = [key for key in check_keys if key not in data]
            if len(missing_keys) > 0:
                raise ValueError(', '.join(missing_keys))
            group = Group.objects.get(id=data['group_id'])
            new_chore_data = {'title': data['title']}
            if 'detail' in data:
                new_chore_data['detail'] = data['detail']
            new_chore = Chore.objects.create(group=group, **new_chore_data)
            return JsonResponse({'id': new_chore.id})
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Group.DoesNotExist:
            return HttpResponseBadRequest('Invalid Group Id')
        except ValueError as e:
            return HttpResponseBadRequest(f'Missing Required body:{e}')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def put(self, request, chore_id):
        """
        Update Chore Detail
        """
        try:
            chore = Chore.objects.get(id=chore_id)
            data = json.loads(request.body)
            editable_str_list = ['title', 'detail', 'completed_date']
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
                    data['completed_date'], '%Y-%m-%dT%H:%M:%S.%f').date()
                print(completed_date)
                setattr(chore, 'completed_date', completed_date)
            if not_changed:
                raise ValueError(
                    'Must have at least one key: title, detail, completed_date')
            chore.save()
            return HttpResponse()
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Chore.DoesNotExist:
            return HttpResponseBadRequest('Invalid chore Id')
        except (ValueError, TypeError)as e:
            return HttpResponseBadRequest(str(e))
        except:
            return HttpResponseServerError('Error is occured. Please try again later')
