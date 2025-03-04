from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'price']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')

        if product.stock < quantity:
            raise serializers.ValidationError(f"{product.name} uchun yetarli mahsulot mavjud emas. Omborda: {product.stock} dona.")

        if quantity <= 0:
            raise serializers.ValidationError("Buyurtma miqdori 1 dan katta bo‘lishi kerak.")

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'status', 'created_at', 'items']

    def validate_customer_email(self, value):
        if "@" not in value or "." not in value:
            raise serializers.ValidationError("To‘g‘ri email manzilini kiriting.")
        return value

    def validate_customer_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Telefon raqami faqat raqamlardan iborat bo‘lishi kerak.")
        if len(value) < 7 or len(value) > 15:
            raise serializers.ValidationError("Telefon raqam uzunligi 7 dan 15 gacha bo‘lishi kerak.")
        return value

    def validate(self, data):
        if data['status'] not in dict(Order.STATUS_CHOICES):
            raise serializers.ValidationError("Noto‘g‘ri buyurtma holati.")

        if len(data['customer_name'].strip()) < 3:
            raise serializers.ValidationError("Mijozning ismi kamida 3 ta harfdan iborat bo‘lishi kerak.")

        return data
