from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import Recipe
from recipe.serializers import RecipeSerializer


RECIPES_URL = reverse('recipe:recipe-list')


def detail_url(recipe_id):
    return reverse('recipe:recipe-detail', args=[recipe_id])


def create_recipe(**params):
    defaults = {
        'name': 'Sample recipe name',
        'description': 'Sample recipe description',
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class RecipeApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_recipes(self):
        create_recipe(name='Breakfast')
        create_recipe(name='Lunch')

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(name='Dinner')

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
