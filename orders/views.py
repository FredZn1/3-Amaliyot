from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer, OrderItemSerializer


class OrderAPIView(APIView):

    def get(self, request, pk=None):
        if pk:
            try:
                order = Order.objects.get(pk=pk)
                serializer = OrderSerializer(order)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Order.DoesNotExist:
                return Response({"error": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        else:
            orders = Order.objects.all().order_by('-created_at')
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            items_data = request.data.get("items", [])
            for item in items_data:
                item["order"] = order.id
                item_serializer = OrderItemSerializer(data=item)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    order.delete()
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
