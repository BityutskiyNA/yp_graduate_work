import pytest

from discount.models import SubscriptionPlan, Subscription, PromotionalCampaign, PromoCode


def test_root_not_found(client):
    response = client.get('/')
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_promo_code(client):
    subscription_plan = SubscriptionPlan.objects.create(
        name='test'
    )
    subscription = Subscription.objects.create(
        name='test',
        subscription_plan=subscription_plan
    )
    promotional_campaign = PromotionalCampaign.objects.create(
        name='test',
        discount_amount=50
    )
    promotional_campaign.subscription.set([subscription])
    pk = promotional_campaign.id
    response = client.post(f'/create/{pk}', {'Quantity': '2', 'Disposable': 'true'})

    promocods = PromoCode.objects.all()
    promocode = promocods[0]

    assert promocode.discount_amount == 50
    assert promocode.discount_percentage == 10
    assert promocode.promotional_campaign == promotional_campaign
    assert promocode.promo_code_type == 'single_use'
    assert len(promocods) == 2
    assert response.status_code == 200


