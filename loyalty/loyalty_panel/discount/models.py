from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class DateTimeMixin(models.Model):
    """Миксин для даты."""

    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubscriptionPlan(DateTimeMixin):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'discount'


class Subscription(DateTimeMixin):
    name = models.CharField(max_length=200)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PromotionalCampaign(DateTimeMixin):
    name = models.CharField(max_length=200)
    discount_amount = models.IntegerField()
    discount_percentage = models.IntegerField()
    validity_period = models.DateField()
    subscription = models.ManyToManyField(Subscription)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'discount'

    def get_fieldsets(self, request):
        fieldsets = super().get_fieldsets(request)
        all_fields = [field.name for field in self._meta.fields]
        new_fieldsets = [(title, {'fields': all_fields}) for title, _ in fieldsets]
        return new_fieldsets

class PromoCode(DateTimeMixin):
    type = [
        ("single_use", "single-use"),
        ("repetitive", "repetitive"),
    ]
    name = models.CharField(max_length=200)
    discount_amount = models.IntegerField(
        validators=[MinValueValidator(1, message='Скидка не может быть отрицательной')])
    discount_percentage = models.IntegerField(validators=[
        MinValueValidator(0, message='Процент скидки не может быть меньше 0'),
        MaxValueValidator(100, message='Процент скидки не может быть больше 100'),
    ])
    promotional_campaign = models.ForeignKey(PromotionalCampaign, on_delete=models.CASCADE)
    validity_period = models.DateField(auto_now_add=True)
    promo_code_type = models.CharField(max_length=50, choices=type)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Discount_History(DateTimeMixin):
    name = models.CharField(max_length=200)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    promotional_campaign = models.ForeignKey(PromotionalCampaign, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return self.name
