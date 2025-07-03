from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    rental_days = forms.IntegerField(min_value=1, initial=1)

class CheckoutForm(forms.ModelForm):
    id_proof = forms.FileField(
        required=True,
        help_text="Upload your government-issued ID (e.g.,Citizenship, License)",
        widget=forms.FileInput(attrs={"accept": ".pdf,.jpg,.jpeg,.png"})
    )

    class Meta:
        model = Order
        fields = ['delivery_method', 'address', 'phone', 'id_proof']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number'}),
        }
