import pytest

from discount.forms import CreateTokenForm


@pytest.mark.django_db
def test_valid_form():
    data = {
        'Quantity': '10',
        'Disposable': True,
    }
    form = CreateTokenForm(data=data)
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_form():
    data = {

    }
    form = CreateTokenForm(data=data)
    assert not form.is_valid()
