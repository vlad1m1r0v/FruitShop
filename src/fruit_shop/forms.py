from django.forms import (
    forms,
    widgets,
    ModelForm
)
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm

from src.fruit_shop.models import Declaration


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control me-lg-2 mb-2 mb-lg-0 w-100',
                'type': 'text',
                'placeholder': 'Username',
                'pattern': r'^[A-Z][a-z]{3,18}\d?$'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control me-lg-2 mb-2 mb-lg-0 w-100',
                'type': 'password',
                'placeholder': 'Password',
                'pattern': r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,20}$'
            }
        )


class DeclarationForm(ModelForm):
    class Meta:
        model = Declaration
        fields = ["file"]

        widgets = {
            "file": widgets.FileInput(attrs={
                "class": "form-control",
                "accept": ".xls,.xlsx"
            })
        }

    def clean_file(self):
        f = self.cleaned_data["file"]
        if not f.name.endswith((".xls", ".xlsx")):
            raise forms.ValidationError("Only Excel files (.xls, .xlsx) are allowed.")
        return f
