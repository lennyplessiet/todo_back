from rest_framework import serializers
from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Le nom de la catégorie ne peut pas être vide.")
        return value

class TaskSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Task
        fields = ['id', 'description', 'is_completed', 'created_at', 'category']

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("La description de la tâche ne peut pas être vide.")
        return value
