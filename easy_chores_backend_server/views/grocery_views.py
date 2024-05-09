from django.views import View
from django.contrib.auth.models import Group, User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.forms.models import model_to_dict
from ..models import Grocery
import json


class GroceryViews(View):

    def get(self, _, grocery_id):
        """
        Get Grocery Detail with Photos
        """
        try:
            grocery = Grocery.objects.get(id=grocery_id)
            grocery_photos = grocery.grocery_photos.all()
            grocery_data = {'grocery': model_to_dict(grocery), 'photos': [
                grocery_photo.photo.url for grocery_photo in grocery_photos]}
            return JsonResponse(grocery_data)
        except Grocery.DoesNotExist:
            return HttpResponseBadRequest('Invalid Grocery Id')

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

    def put(self, request, grocery_id):
        """
        Update Grocery Detail
        """
        try:
            grocery = Grocery.objects.get(id=grocery_id)
            data = json.loads(request.body)
            editable_list = ['name', 'detail', 'quantity']
            not_changed = True
            for key in editable_list:
                if key in data:
                    not_changed = False
                    setattr(grocery, key, data[key])
            if not_changed:
                raise ValueError(
                    'Must have at least one key: name, detail, quantity')
            grocery.save()
            return HttpResponse()
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Grocery.DoesNotExist:
            return HttpResponseBadRequest('Invalid Grocery Id')
        except ValueError as e:
            return HttpResponseBadRequest(str(e))
