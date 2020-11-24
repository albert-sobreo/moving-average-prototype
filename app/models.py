from django.db import models

# Create your models here.
class Inventory(models.Model):
    name = models.CharField(max_length=128)
    total_quantity = models.IntegerField()
    current_ppi = models.FloatField()
    total_cost = models.FloatField()

    class Meta:
        db_table = "Inventory"
        verbose_name_plural = "Inventory"

    def __str__(self):
        return self.name


class Purchase(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost_per_item = models.FloatField()
    total_cost = models.FloatField()

    class Meta:
        db_table = "Purchase"
        verbose_name_plural = "Purchase"

    def __str__(self):
        return self.inventory.name + " qty: " + str(self.quantity)


class Sales(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cost_per_item = models.FloatField()
    total_cost = models.FloatField()

    class Meta:
        db_table = "Sales"
        verbose_name_plural = "Sales"

    def __str__(self):
        return self.inventory.name + " qty: " + str(self.quantity)