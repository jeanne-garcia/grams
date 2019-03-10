from django.forms import ModelForm
from .models import Vendors


class AddVendorForm(ModelForm):
    class Meta:
        model = Vendors
        fields = ['name', 'address', 'contact_number', 'contact_email']


class EditVendorForm(ModelForm):
    class Meta:
        model = Vendors
        fields = fields = ['name', 'address', 'contact_number', 'contact_email']