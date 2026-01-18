from django.db import models

# Create your models here.
class Unit(models.Model):
    name = models.CharField()
    name_plural = models.CharField(blank=True)
    short = models.CharField(blank=True)

    def __str__(self):
        return self.short if self.short else self.name
    
    def plural_str(self):
        return self.name_plural if self.name_plural else self.__str__()
    

class Food(models.Model):
    name = models.CharField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} ({self.unit})"


class Recipe(models.Model):
    name = models.CharField()
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Food, on_delete=models.PROTECT)
    amount = models.IntegerField()
    comment = models.CharField(blank=True)

    def __str__(self):
        return f"""{self.amount} {self.ingredient.unit.plural_str() if self.amount > 1 else self.ingredient.unit} 
            {self.ingredient.name} ({self.recipe})"""
