from rest_framework.viewsets import ModelViewSet

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.order_by('-id')
