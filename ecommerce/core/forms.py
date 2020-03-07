from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_OPTIONS = (
	('P', 'Paypal'),
	('S', 'Stripe')
)

class CheckoutForm(forms.Form):
	address = forms.CharField(widget=forms.TextInput(attrs={
			'placeholder':'1234 Main St',
			'class':'form-control'
		}))
	appartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'placeholder':'Apartment or suit',
			'class':'form-control'			
		}))	
	country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
		'class':'custom-select d-block w-100'
		}))
	zip = forms.CharField(max_length=100, widget=forms.TextInput(attrs=({
			'class': 'form-control'
		})))	
	same_shipping_address = forms.BooleanField(required=False)
	save_info = forms.BooleanField(required=False)
	payment_options = forms.ChoiceField(choices=PAYMENT_OPTIONS, widget=forms.RadioSelect())