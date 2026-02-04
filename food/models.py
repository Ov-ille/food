from django.db import models
from django.db.models import UniqueConstraint, constraints

# Create your models here.
class Unit(models.Model):
    name = models.CharField()
    name_plural = models.CharField(blank=True)
    short = models.CharField(blank=True)

    class Meta:
        constraints = [
            UniqueConstraint("name", name="unique_unit_name")
        ]

    def __str__(self):
        return self.short if self.short else self.name
    
    def plural_str(self):
        return self.name_plural if self.name_plural else self.__str__()
    

class Food(models.Model):
    name = models.CharField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["name", "unit"], name="unique_food")
        ]
    
    def __str__(self):
        return f"{self.name} ({self.unit})"


class Recipe(models.Model):
    name = models.CharField()
    instructions = models.TextField(blank=True)
    portions = models.IntegerField(default=1)

    class Meta:
        constraints = [
            UniqueConstraint("name", name="unique_recipe_name")
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.PROTECT)
    amount = models.IntegerField()
    comment = models.CharField(blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["recipe", "food"], name="unique_ingredient")
        ]

    def __str__(self):
        return f"""{self.amount} {self.food.unit.plural_str() if self.amount > 1 else self.food.unit} 
            {self.food.name} ({self.recipe})"""

    def amount_per_portion(self):
        return self.amount / self.recipe.portions