from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpResponse, HttpRequest
from django.db import transaction
from ..models import User
import json


@require_POST
def register(request):
    try:
        with transaction.atomic():
            data: dict[str] = json.loads(request.body)
            check_keys = ['username', 'password', 'email']
            missing_keys = [key for key in check_keys if key not in data]
            if len(missing_keys) > 0:
                raise ValueError(', '.join(missing_keys))
            print("Hi1")
            user = User.objects.create_user(
                username=data['username'], email=data['email'], password=data['password'])
            print("Hi2")
            return JsonResponse({'access_token': ""})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Required JSON body data')
    except ValueError as e:
        return HttpResponseBadRequest(f'Missing Required body:{e}')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


@require_POST
def login(request):
    try:
        data: dict[str] = json.loads(request.body)
        check_keys = ['password', 'email']
        missing_keys = [key for key in check_keys if key not in data]
        if len(missing_keys) > 0:
            raise ValueError(', '.join(missing_keys))
        user = User.objects.get(email=data['email'])
        if not user.check_password(data['password']):
            raise AssertionError()
        return JsonResponse({'access_token': ""})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Required JSON body data')
    except ValueError as e:
        return HttpResponseBadRequest(f'Missing Required body:{e}')
    except AssertionError:
        return HttpResponseBadRequest('Invalid password', status=401)
    except:
        return HttpResponseServerError('Error is occured. Please try again later')
