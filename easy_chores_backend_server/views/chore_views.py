from django.views import View
from ..models import Chore


class ChoreViews(View):
    def get(self, request, chore_id):
        pass
