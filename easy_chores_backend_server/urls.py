from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views.group_views import GroupUserViews, get_grocery_list, get_chore_list, create_group
from .views.grocery_views import GroceryViews

urlpatterns = [
    path('group', create_group),
    path('group/<int:group_id>/groceries', get_grocery_list),
    path('group/<int:group_id>/chores', get_chore_list),
    path('groups/<int:group_id>/users', GroupUserViews.as_view()),
    path('groups/<int:group_id>/user/<int:user_id>', GroupUserViews.as_view()),
    path('grocery', GroceryViews.as_view())]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
