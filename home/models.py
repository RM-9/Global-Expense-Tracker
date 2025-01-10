from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_foreign = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name=models.CharField(max_length=60, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=200)
    amount = models.FloatField()
    from_currency = models.CharField(max_length=10 )  # e.g., 'USD', 'EUR', etc.
    converted_amount = models.FloatField(null=True, blank=True)
    #category_choises=[('Travel','Travel'),('Stay','Stay'),('Food','Food'),('Other','Other')]
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} - {self.amount} {self.from_currency}"

