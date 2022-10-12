from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)
    recipe = models.ForeignKey(
        'Recipe',
        related_name='ingredients',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
