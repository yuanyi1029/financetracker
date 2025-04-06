from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Record(models.Model):
    CATEGORY_CHOICES = [
        (1, "Food & Drinks"),
        (2, "Shopping"),
        (3, "Housing"),
        (4, "Transportation"),
        (5, "Vehicle"),
        (6, "Life & Entertainment"),
        (7, "Communication, Technology"),
        (8, "Financial Expenses"),
        (9, "Investments"),
        (10, "Income"),
        (11, "Others"),
        (0, "Planned Payment")
    ]

    TYPE_CHOICES = [
        (1, "Income"),
        (2, "Expense"),
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="record_user")
    record_type = models.PositiveIntegerField(choices=TYPE_CHOICES)
    category = models.PositiveIntegerField(choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=64, blank=True)
    time = models.DateTimeField(auto_now_add=False)

class Planned(models.Model):
    TYPE_CHOICES = [
        (1, "Income"),
        (2, "Expense"),
    ]

    FREQUENCY_CHOICES = [
        (1, "One-time"),
        (2, "Recurrent")
    ]

    RECURRENCE_CHOICES = [
        (1, "Daily"),
        (2, "Weekly"),
        (3, "Monthly"),
        (4, "Anually")
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="planned_user")
    planned_type = models.PositiveIntegerField(choices=TYPE_CHOICES)
    frequency = models.PositiveIntegerField(choices=FREQUENCY_CHOICES)
    recurrence = models.PositiveIntegerField(choices=RECURRENCE_CHOICES, blank=True, null=True)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=False)