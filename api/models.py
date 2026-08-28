from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(blank=False, null=False, unique=True, default="")

    def __str__(self):
        return f"{self.name} ({self.id})"

class Task(models.Model):
    description = models.TextField(blank=False, null=False, default="")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.description} ({self.id})"
    