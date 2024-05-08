from django.views import View
from django.contrib.auth.models import Group, User
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from ..models import Grocery
import json


class GroceryViews(View):

    def post(self, request):
        """
        Create Grocery item
        """
        try:
            data = json.loads(request.body)
            check_keys = ['user_id', 'group_id', 'name']
            missing_keys = [key for key in check_keys if key not in data]
            if len(missing_keys) > 0:
                raise ValueError(', '.join(missing_keys))
            creator = User.objects.get(id=data['user_id'])
            group = Group.objects.get(id=data['group_id'])
            new_grocery_data = {
                'creator': creator,
                'group': group,
                'name': data['name'],
            }
            if 'quantity' in data:
                new_grocery_data['quantity'] = data['quantity']
            if 'detail' in data:
                new_grocery_data['detail'] = data['detail']
            new_grocery = Grocery.objects.create(**new_grocery_data)
            return JsonResponse({'grocery_id': new_grocery.id})
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Group.DoesNotExist:
            return HttpResponseBadRequest('Invalid Group Id')
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid User Id')
        except ValueError as e:
            return HttpResponseBadRequest(f'Missing Required body:{e}')
