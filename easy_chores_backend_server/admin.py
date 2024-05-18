from django.contrib import admin
from .models import Chore, Grocery, GroceryPhoto, User

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active', 'username')
    list_filter = ('email', 'is_staff', 'is_active', 'groups', 'username')
    fieldsets = (
        (None, {'fields': ('email', 'password',
         'first_name', 'last_name', 'username')}),
        ('Permissions', {'fields': ('is_staff',
         'is_active', 'groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups', 'username')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(Chore)
class ChoresAdmin(admin.ModelAdmin):
    pass


@admin.register(Grocery)
class GroceryAdmin(admin.ModelAdmin):
    pass


@admin.register(GroceryPhoto)
class GroceryPhotoAdmin(admin.ModelAdmin):
    pass
