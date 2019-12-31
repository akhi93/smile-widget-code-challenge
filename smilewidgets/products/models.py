from django.db import models

from .utils import is_black_friday, is_2019


class Product(models.Model):
    name = models.CharField(max_length=25, help_text="Customer facing name of product")
    code = models.CharField(
        max_length=10, help_text="Internal facing reference to product"
    )
    price = models.PositiveIntegerField(help_text="Price of product in cents")

    def __str__(self):
        return "{} - {}".format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text="Value of gift card in cents")
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return "{} - {}".format(self.code, self.formatted_amount)

    def is_valid(self, date):
        return ((not self.date_start) or self.date_start <= date) and (
            (not self.date_end) or self.date_end >= date
        )

    @property
    def formatted_amount(self):
        return "${0:.2f}".format(self.amount / 100)


class ProductPrice(models.Model):
    """Model definition for ProductPrice."""

    PRICE_SCHEDULES = (("black_friday", "Black Friday"), ("2019_prices", "2019 Prices"))

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    schedule_name = models.CharField(
        "Price Schedule", max_length=15, choices=PRICE_SCHEDULES
    )
    price = models.IntegerField("Product Price", help_text="Price of product in cents")

    class Meta:
        """Meta definition for ProductPrice."""

        verbose_name = "ProductPrice"
        verbose_name_plural = "ProductPrices"

    def __str__(self):
        """Unicode representation of ProductPrice."""
        return "{} - {} - {}".format(
            self.scheule_name, str(self.product.name), str(self.price)
        )

    @classmethod
    def get_schedule(cls, date, product):
        # Its not appropriate to store schedule start date and end dates
        # database as black friday is year independent
        query = None
        if is_black_friday(date):
            query = ProductPrice.objects.filter(schedule_name="Black Friday")
        if is_2019(date):
            query = ProductPrice.objects.filter(schedule_name="2019 Prices")

        if query:
            return query.filter(product=product).first()

    @property
    def formatted_amount(self):
        return "${0:.2f}".format(self.price / 100)
