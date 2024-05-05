from django.db import models


class GroceryPhoto(models.Model):
    grocery = models.ForeignKey(
        'Grocery', on_delete=models.CASCADE, related_name='grocery_photos')
    photo = models.ImageField(upload_to='grocery_photos/')

    def __str__(self):
        return f"{self.url}"
