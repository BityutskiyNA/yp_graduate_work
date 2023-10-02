from django.shortcuts import render, redirect

from .forms import CreateTokenForm
from .services import CreatesPromoCodes


def create_token_view(request, pk):
    if request.method == 'POST':
        form = CreateTokenForm(request.POST)
        if form.is_valid():
            quantity = request.POST['Quantity']
            disposable = bool(request.POST['Disposable'])
            promo = CreatesPromoCodes(quantity, disposable)
            promo.set_promotional_campaign(pk)
            previous_url = request.META.get('HTTP_ORIGIN')
            if previous_url:
                return redirect(f'{previous_url}/admin/discount/promotionalcampaign/{pk}/change/')
    else:
        form = CreateTokenForm()

    return render(request, 'token_creation.html', {'form': form})
