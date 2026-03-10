from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'Draft', 'Draft'
        APPROVED = 'Approved', 'Approved'

    product_id = models.IntegerField(unique=True, validators=[MinValueValidator(1)])
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-last_updated']

    def __str__(self) -> str:
        return f'{self.product_id} - {self.name}'
