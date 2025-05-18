from django import forms
from django.core.exceptions import ValidationError
from .models import User

class ManagerCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'country']
        labels = {
            'first_name': 'Name',
            'email': 'Email',
            'country': 'Country',
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("This email is already used for another account.")
        return email
