from django.forms import ModelForm
from App_Payment.models import BillingAddress

class CheckoutAddress(ModelForm):
    class Meta:
        model = BillingAddress
        exclude = ('user',)
    