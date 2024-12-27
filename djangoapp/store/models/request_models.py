from django.db import models
from django.contrib.auth.models import User


class Requests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aproved'),
            ('C', 'Created'),
            ('R', 'Reproved'),
            ('P', 'Pending'),
            ('S', 'Sent'),
            ('F', 'Finalized'),
        )
    )

    def __str__(self) -> str:
        return f'Request N. {self.pk}'

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'


class ItemRequest(models.Model):
    request = models.ForeignKey(Requests, on_delete=models.CASCADE)
    product = models.CharField(max_length=55)
    product_id = models.PositiveIntegerField()
    productType = models.CharField(max_length=55)
    productType_id = models.PositiveIntegerField()
    price = models.FloatField()
    promo_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField()
    image = models.CharField(max_length=2000)

    def __str__(self):
        return f'Item of {self.request}'

    class Meta:
        verbose_name = 'Item Request'
        verbose_name_plural = 'Items of Request'
