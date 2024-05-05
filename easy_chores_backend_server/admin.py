from django.contrib import admin
from .models import Chore, Grocery, GroceryPhoto

# Register your models here.


@admin.register(Chore)
class ChoresAdmin(admin.ModelAdmin):
    pass


@admin.register(Grocery)
class GroceryAdmin(admin.ModelAdmin):
    pass


@admin.register(GroceryPhoto)
class GroceryPhotoAdmin(admin.ModelAdmin):
    pass
