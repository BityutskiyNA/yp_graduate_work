from django.contrib import admin

from discount.models import PromotionalCampaign, PromoCode, \
    Discount_History, Subscription, SubscriptionPlan
from django.utils.html import format_html


class PromotionalCampaignPromoCode(admin.TabularInline):
    model = PromoCode
    extra = 1


@admin.register(PromotionalCampaign)
class PromotionalCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'validity_period', 'active', 'created')
    inlines = [PromotionalCampaignPromoCode]

    def send_button(self, obj):
        process_url = f"/create/{obj.pk}"
        button_html = '<a class="button" href="{}"><img src="/path/to/process_icon.png" alt="Create promo code" /></a>'.format(
            process_url)
        return format_html(button_html)

    send_button.short_description = ''

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj:
            fieldsets += (
                ('Create Button', {
                    'fields': (),
                    'description': self.send_button(obj)
                }),
            )
        return fieldsets


admin.site.register(PromoCode)
admin.site.register(Subscription)
admin.site.register(SubscriptionPlan)
admin.site.register(Discount_History)
