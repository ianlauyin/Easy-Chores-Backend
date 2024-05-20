from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseServerError
from django.db import transaction
from django.core.cache import cache
from django.db.utils import IntegrityError
from ..models import User
from jwt.exceptions import DecodeError
import json
import jwt
import os


@require_POST
def register(request):
    try:
        with transaction.atomic():
            data: dict[str] = json.loads(request.body)
            check_keys = ['username', 'password', 'email']
            missing_keys = [key for key in check_keys if key not in data]
            if len(missing_keys) > 0:
                raise ValueError(', '.join(missing_keys))
            user = User.objects.create_user(
                username=data['username'], email=data['email'], password=data['password'])
            access_token = user.generate_access_token()
            return JsonResponse({'access_token': access_token, 'user_id': user.id, 'username': user.username})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Required JSON body data')
    except IntegrityError:
        return HttpResponseBadRequest("A user with that email already exists.")
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
        access_token = user.generate_access_token()
        return JsonResponse({'access_token': access_token, 'user_id': user.id, 'username': user.username})
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Required JSON body data')
    except ValueError as e:
        return HttpResponseBadRequest(f'Missing Required body:{e}')
    except (AssertionError, User.DoesNotExist):
        return HttpResponseBadRequest('Invalid password', status=401)
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


def verify_token(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                raise ValueError('No access token provided')
            decoded_jwt = jwt.decode(token, os.getenv(
                'TOKEN_SECRET'), algorithms=["HS256"])
            if 'user_id' not in decoded_jwt:
                raise ValueError('Invalid Token')
            user_id = decoded_jwt['user_id']
            checkToken = cache.get(f'access_token_{user_id}')
            if checkToken is None:
                raise TimeoutError()
            User.objects.get(id=user_id)
        except ValueError as e:
            return HttpResponseBadRequest(str(e), status=401)
        except TimeoutError:
            return HttpResponseBadRequest('Expired Token', status=401)
        except (User.DoesNotExist, DecodeError):
            return HttpResponseBadRequest('Invalid Token', status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
