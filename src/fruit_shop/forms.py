from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {
                'class': 'form-control me-lg-2 mb-2 mb-lg-0 w-100',
                'type': 'text',
                'placeholder': 'Username',
                'pattern': '^[A-Z][a-z]{3,18}\d?$'
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control me-lg-2 mb-2 mb-lg-0 w-100',
                'type': 'password',
                'placeholder': 'Password',
                'pattern': '^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,20}$'
            }
        )
