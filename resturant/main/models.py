from django.db import models

# Create your models here.
#Ingredents in inventory
class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_units = models.IntegerField()

    def __str__(self):
        return self.name

#A list of ingredents each menu item requires
class RecipeRequirement(models.Model):
    ingredents = models.ManyToManyField('Ingredient', related_name='recipe_requirements')


#MenuItems 
class MenuItem(models.Model):
    recipe_name =models.CharField(max_length=50, unique=True)
    recipe_requirements = models.ForeignKey(RecipeRequirement , on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places = 2)

#Purchases
class Purchase(models.Model):
    created_at = models.DateField(auto_now_add=True)
    items = models.ManyToManyField('MenuItem', related_name='purchases', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    #save purchase and update inventory
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for purchase_item in self.purchase_item.all():
            quantity = purchase_item.quantity
            item = purchase_item.item

            for ingredient in item.recipe_requirements.ingredients.all():
                ingredient.available_units -= quantity
                ingredient.save()





class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase,related_name='purchase_item', on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)