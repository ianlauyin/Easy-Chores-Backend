from django.views import View
from django.contrib.auth.models import Group
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, HttpResponseServerError, HttpResponseNotFound, HttpRequest
from django.forms.models import model_to_dict
from django.db import transaction
from django.db.models.query import QuerySet
from ..models import Grocery, User
from ..views.auth_views import verify_token
from django.utils.decorators import method_decorator
import json
import os


@method_decorator(verify_token, name='dispatch')
class GroceryViews(View):

    def get(self, _, grocery_id: int):
        """
        Get Grocery Detail with Photos
        """
        try:
            grocery = Grocery.objects.get(id=grocery_id)
            grocery_photos: QuerySet = grocery.grocery_photos.all()
            grocery_data = {'grocery': model_to_dict(grocery), 'photos': [
                grocery_photo.photo.url for grocery_photo in grocery_photos]}
            return JsonResponse(grocery_data)
        except Grocery.DoesNotExist:
            return HttpResponseNotFound('Invalid Grocery Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def post(self, request: HttpRequest):
        """
        Create Grocery item
        """
        try:
            data: dict[str] = json.loads(request.body)
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
            optional_keys = ['quantity', 'detail']
            for key in optional_keys:
                if key in data:
                    new_grocery_data[key] = data[key]
            new_grocery = Grocery.objects.create(**new_grocery_data)
            return JsonResponse({'grocery_id': new_grocery.id}, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Group.DoesNotExist:
            return HttpResponseNotFound('Invalid Group Id')
        except User.DoesNotExist:
            return HttpResponseNotFound('Invalid User Id')
        except ValueError as e:
            return HttpResponseBadRequest(f'Missing Required body:{e}')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def put(self, request: HttpRequest, grocery_id: int):
        """
        Update Grocery Detail
        """
        try:
            grocery = Grocery.objects.get(id=grocery_id)
            data: dict[str] = json.loads(request.body)
            editable_str_list = ['name', 'detail']
            not_changed = True
            for key in editable_str_list:
                if key in data:
                    if not isinstance(data[key], str):
                        raise TypeError(
                            f'Required string type of key: {key}')
                    not_changed = False
                    setattr(grocery, key, data[key])
            if 'quantity' in data:
                if not isinstance(data['quantity'], int):
                    raise TypeError(f'Required int type of key: quantity')
                not_changed = False
                setattr(grocery, 'quantity', data['quantity'])
            if not_changed:
                raise ValueError(
                    'Must have at least one key: name, detail, quantity')
            grocery.save()
            return HttpResponse(status=204)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Required JSON body data')
        except Grocery.DoesNotExist:
            return HttpResponseNotFound('Invalid Grocery Id')
        except (ValueError, TypeError) as e:
            return HttpResponseBadRequest(str(e))
        except:
            return HttpResponseServerError('Error is occured. Please try again later')

    def delete(self, _, grocery_id: int):
        """
        Delete Grocery Item along with photos
        """
        try:
            with transaction.atomic():
                grocery = Grocery.objects.get(id=grocery_id)
                grocery_photos = grocery.grocery_photos.all()
                for grocery_photo in grocery_photos:
                    if os.path.exists(grocery_photo.photo.path):
                        os.remove(grocery_photo.photo.path)
                    grocery_photo.delete()
                grocery.delete()
                return HttpResponse(status=204)
        except Grocery.DoesNotExist:
            return HttpResponseNotFound('Invalid Grocery Id')
        except:
            return HttpResponseServerError('Error is occured. Please try again later')
