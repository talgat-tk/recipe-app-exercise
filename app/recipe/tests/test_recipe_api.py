from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from recipe.models import (
    Recipe,
    Ingredient,
)
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

    def test_create_recipe(self):
        payload = {
            'name': 'Breakfast',
            'description': 'Eggs + Toast',
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        recipe = Recipe.objects.get(id=res.data['id'])
        serializer = RecipeSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_delete_recipe(self):
        recipe = create_recipe(name='Lunch')

        url = detail_url(recipe.id)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        exists = Recipe.objects.filter(id=recipe.id)
        self.assertFalse(exists)

    def test_patch_recipe(self):
        name = 'Dinner'
        recipe = create_recipe(name=name)

        url = detail_url(recipe.id)
        payload = {
            'description': 'Description for dinner'
        }

        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, name)
        self.assertEqual(recipe.description, payload['description'])

    def test_put_recipe_incomplete(self):
        initial = {
            'name': 'Breakfast',
            'description': 'Description for breakfast',
        }
        recipe = create_recipe(**initial)

        url = detail_url(recipe.id)
        payload = {
            'description': 'Incorrect payload description'
        }

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, initial['name'])
        self.assertEqual(recipe.description, initial['description'])

    def test_put_recipe(self):
        initial = {
            'name': 'Lunch',
            'description': 'Description for lunch',
        }
        recipe = create_recipe(**initial)

        url = detail_url(recipe.id)
        payload = {
            'name': 'Dinner',
            'description': 'Description for dinner',
        }

        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(recipe.name, payload['name'])
        self.assertEqual(recipe.description, payload['description'])

    def test_create_recipe_with_ingredients(self):
        payload = {
            'name': 'Breakfast',
            'description': 'Description for breakfast',
            'ingredients': [{
                'name': 'Eggs',
            }, {
                'name': 'Toast',
            }]
        }

        res = self.client.post(RECIPES_URL, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for ingredient in payload['ingredients']:
            self.assertIn(ingredient, res.data['ingredients'])

    def test_patch_recipe_with_ingredients(self):
        recipe = create_recipe(
            name='Breakfast',
            description='Good recipe',
        )
        Ingredient.objects.create(name='Eggs', recipe=recipe)
        Ingredient.objects.create(name='Toast', recipe=recipe)

        payload = {
            'ingredients': [
                {'name': 'Coffee'},
            ]
        }

        url = detail_url(recipe.id)

        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe.refresh_from_db()
        self.assertEqual(len(recipe.ingredients.all()), 1)
        for ingredient in payload['ingredients']:
            exists = recipe.ingredients.filter(
                name=ingredient['name']
            ).exists()
            self.assertTrue(exists)

    def test_delete_recipe_with_ingredients(self):
        recipe = create_recipe(
            name='Lunch',
            description='Lunch recipe',
        )
        Ingredient.objects.create(name='Soup', recipe=recipe)
        Ingredient.objects.create(name='Steak', recipe=recipe)

        url = detail_url(recipe.id)
        self.client.delete(url)

        self.assertEqual(len(recipe.ingredients.all()), 0)
