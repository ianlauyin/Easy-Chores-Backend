
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from ..models import GroceryPhoto, Grocery
import os


@require_http_methods(['DELETE'])
def delete_grocery_photo(request, photo_id):
    """
    Delete a photo from db and media
    """
    try:
        photo = GroceryPhoto.objects.get(id=photo_id)
        if os.path.exists(photo.photo.path):
            os.remove(photo.photo.path)
        photo.delete()
        return HttpResponse()
    except GroceryPhoto.DoesNotExist:
        return HttpResponseBadRequest('Invalid photo id')
    except:
        return HttpResponseServerError('Error is occured. Please try again later')


@require_http_methods(["POST"])
def add_grocery_photo(request, grocery_id):
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
        return HttpResponseBadRequest('Invalid grocery id')
    except ValueError as e:
        return HttpResponseBadRequest(str(e))
    except:
        return HttpResponseServerError('Error is occured. Please try again later')
