from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .serializers import PriceSerializer
from .models import ProductPrice


class GetPriceView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        ser = PriceSerializer(data=request.query_params)

        if not ser.is_valid():
            return Response(ser.errors, status=400)

        product = ser.validated_data["productCode"]
        date = ser.validated_data["date"]
        giftcard = ser.validated_data.get("giftCardCode")

        schedule = ProductPrice.get_schedule(date, product)

        price = product.price
        if schedule:
            price = schedule.price

        if giftcard and giftcard.is_valid(date):
            price -= giftcard.amount

        # price should not be -ve in any case
        if price < 0:
            price = 0

        resp = {
            key: request.query_params.get(key)
            for key in ["productCode", "date", "giftCardCode"]
        }
        resp["price"] = "${0:.2f}".format(price / 100)

        return Response(resp)
