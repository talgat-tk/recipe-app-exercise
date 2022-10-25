from rest_framework.viewsets import ModelViewSet

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        name = self.request.query_params.get('name')

        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__istartswith=name)

        return queryset.order_by('-id')
