from django.db import models
from categories.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = (
            models.Index(fields=['category', 'name']),
        )
        unique_together = (('category', 'name'), )

    def __str__(self):
        return f"Product: {self.name}"