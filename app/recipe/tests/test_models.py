from django.test import TestCase

from recipe import models


class ModelTest(TestCase):
    def test_create_recipe(self):
        params = {
            'name': 'Recipe Name',
            'description': 'Sample Description',
        }

        recipe = models.Recipe.objects.create(**params)

        self.assertEqual(str(recipe), recipe.name)
