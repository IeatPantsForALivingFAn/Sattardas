from django import forms
from .models import Donation
#form classes

class DonorCreateForm(forms.ModelForm):
   
   class Meta:
       model = Donation
       fields = ['name','amount']