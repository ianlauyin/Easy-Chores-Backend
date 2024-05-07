from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views.group_user_views import GroupUserViews

urlpatterns = [
    path('groups/<int:group_id>/users', GroupUserViews.as_view()),
    path('groups/<int:group_id>/user/<int:user_id>', GroupUserViews.as_view())]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
