
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseServerError, HttpResponseNotFound, HttpRequest
from django.views.decorators.http import require_http_methods
from ..models import GroceryPhoto, Grocery
from ..views.auth_views import verify_token
import os


@require_http_methods(['DELETE'])
@verify_token
def delete_grocery_photo(_, photo_id):
    """
    Delete a photo from db and media
    """
    try:
        photo = GroceryPhoto.objects.get(id=photo_id)
        if os.path.exists(photo.photo.path):
            os.remove(photo.photo.path)
        photo.delete()
        return HttpResponse(status=204)
    except GroceryPhoto.DoesNotExist:
        return HttpResponseNotFound('Invalid photo id')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


@require_http_methods(["POST"])
@verify_token
def add_grocery_photo(request: HttpRequest, grocery_id: int):
    """
    Add a photo to grocery
    """
    try:
        new_photo = request.FILES.get('photo')
        if new_photo is None:
            raise ValueError('Missing Requied file: photo')
        type_list = ['.jpg', '.jpeg', '.png', '.bmp']
        file_type = os.path.splitext(new_photo.name)[1].lower()
        if file_type not in type_list:
            raise ValueError('Wrong Type of Photo')
        grocery = Grocery.objects.get(id=grocery_id)
        grocery_photo = GroceryPhoto.objects.create(
            grocery=grocery, photo=new_photo)
        grocery_photo_data = {'id': grocery_photo.id,
                              'url': grocery_photo.photo.url,
                              'path': grocery_photo.photo.path}
        return JsonResponse(grocery_photo_data)
    except Grocery.DoesNotExist:
        return HttpResponseNotFound('Invalid grocery id')
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    except:
        return HttpResponseServerError('Error is occured. Please try again later')
