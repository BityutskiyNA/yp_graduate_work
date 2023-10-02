from discount.models import PromotionalCampaign, PromoCode
import random
import string


class CreatesPromoCodes:
    def __init__(self, quantity, disposable):
        self.quantity = int(quantity)
        self.disposable = disposable
        self.promotional_campaign = None

    def set_promotional_campaign(self, pk):
        self.promotional_campaign = PromotionalCampaign.objects.get(pk=pk)
        self.create_promo_codes()

    def generate_code(self):
        letters = string.ascii_lowercase
        rand_string = ''.join(random.choice(letters) for i in range(12))
        return rand_string

    def create_promo_codes(self):
        promo = 1
        while promo <= self.quantity:
            promo_code = PromoCode()
            promo_code.name = self.generate_code()
            promo_code.promotional_campaign = self.promotional_campaign
            if self.disposable:
                promo_code.promo_code_type = 'single_use'
            else:
                promo_code.promo_code_type = 'repetitive'
            promo_code.validity_period = self.promotional_campaign.validity_period
            promo_code.discount_amount = self.promotional_campaign.discount_amount
            promo_code.discount_percentage = self.promotional_campaign.discount_percentage
            promo_code.save()
            promo += 1
