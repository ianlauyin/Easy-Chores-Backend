from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreationForm(UserCreationForm):

    def save(self, commit=True):
        user = self.instance
        if user.is_staff:
            user.is_superuser = True
        return super().save(commit=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
