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

    def test_create_ingredient(self):
        recipe = models.Recipe.objects.create(
            name='Breakfast',
            description='Description for breakfast',
        )

        ingredient = models.Ingredient.objects.create(
            name='Eggs',
            recipe=recipe,
        )

        self.assertEqual(str(ingredient), ingredient.name)
        self.assertEqual(ingredient.recipe, recipe)
        self.assertIn(ingredient, recipe.ingredient_set.all())
