from rest_framework import serializers
from .models import Product, GiftCard


class PriceSerializer(serializers.Serializer):
    date = serializers.DateField()
    productCode = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="code"
    )
    giftCardCode = serializers.SlugRelatedField(
        queryset=GiftCard.objects.all(),
        required=False,
        slug_field="code",
    )
