from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_name', 'quantity', 'price']

    def validate(self, data):
        errors = {}

        product = data.get('product')
        quantity = data.get('quantity')

        if product and quantity:
            if product.stock < quantity:
                errors['quantity'] = f"{product.name} uchun yetarli mahsulot mavjud emas. Omborda: {product.stock} dona."

            if quantity <= 0:
                errors['quantity'] = "Buyurtma miqdori 1 dan katta bo‘lishi kerak."

        price = data.get('price')
        if price is not None and price < 0:
            errors['price'] = "Narx manfiy bo‘lishi mumkin emas."

        if errors:
            raise serializers.ValidationError(errors)

        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'total_price', 'status', 'created_at', 'items']

    def validate(self, data):
        errors = {}

        if data.get('status') not in dict(Order.STATUS_CHOICES):
            errors['status'] = "Noto‘g‘ri buyurtma holati."

        # Mijozning ismi tekshiriladi
        if 'customer_name' in data and len(data['customer_name'].strip()) < 3:
            errors['customer_name'] = "Mijozning ismi kamida 3 ta harfdan iborat bo‘lishi kerak."

        # Mijozning email manzili tekshiriladi
        if 'customer_email' in data:
            email = data['customer_email']
            if "@" not in email or "." not in email:
                errors['customer_email'] = "To‘g‘ri email manzilini kiriting."

        if 'customer_phone' in data:
            phone = data['customer_phone']
            if not phone.isdigit():
                errors['customer_phone'] = "Telefon raqami faqat raqamlardan iborat bo‘lishi kerak."
            elif len(phone) < 7 or len(phone) > 15:
                errors['customer_phone'] = "Telefon raqam uzunligi 7 dan 15 gacha bo‘lishi kerak."

        if errors:
            raise serializers.ValidationError(errors)

        return data
