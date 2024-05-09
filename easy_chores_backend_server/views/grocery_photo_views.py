from django.views import View
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from ..models import GroceryPhoto
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
