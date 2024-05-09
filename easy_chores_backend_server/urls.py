from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views.group_views import GroupUserViews, get_grocery_list, get_chore_list, create_group
from .views.grocery_views import GroceryViews
from .views.grocery_photo_views import delete_grocery_photo, add_grocery_photo

urlpatterns = [
    path('groups', create_group),
    path('groups/<int:group_id>/groceries', get_grocery_list),
    path('groups/<int:group_id>/chores', get_chore_list),
    path('groups/<int:group_id>/users', GroupUserViews.as_view()),
    path('groups/<int:group_id>/users/<int:user_id>', GroupUserViews.as_view()),
    path('groceries', GroceryViews.as_view()),
    path('groceries/<int:grocery_id>', GroceryViews.as_view()),
    path('groceries/<int:grocery_id>/photos', add_grocery_photo),
    path('groceries/photos/<int:photo_id>', delete_grocery_photo),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
