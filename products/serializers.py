from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category']

    def validate(self, data):

        if not data.get("name") or len(data["name"]) < 3:
            raise serializers.ValidationError({"name": "Nom kamida 3 ta belgidan iborat bo‘lishi kerak!"})

        if not data.get("description") or len(data["description"]) < 10:
            raise serializers.ValidationError({"description": "Tavsif kamida 10 ta belgidan iborat bo‘lishi kerak!"})

        if data.get("price", 0) < 0:
            raise serializers.ValidationError({"price": "Narx manfiy bo‘lishi mumkin emas!"})

        if data.get("stock", 0) < 0:
            raise serializers.ValidationError({"stock": "Ombor zaxirasi (stock) 0 dan kam bo‘lishi mumkin emas!"})

        if not data.get("category"):
            raise serializers.ValidationError({"category": "Kategoriya tanlash majburiy!"})

        return data
