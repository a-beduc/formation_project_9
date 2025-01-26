from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63,
                               label="",
                               widget=forms.TextInput(
                                   attrs={"placeholder": "Nom d'utilisateur",
                                          "class": 'loginBlock__input'}
                                )
                               )
    password = forms.CharField(max_length=63,
                               label="",
                               widget=forms.PasswordInput(
                                   attrs={"placeholder": "Mot de passe",
                                          "class": 'loginBlock__input'}
                                )
                               )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''

        self.fields['username'].widget.attrs.update({
            'placeholder': "Nom d'utilisateur",
            'class': 'signupPage__input',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': "Mot de passe",
            'class': 'signupPage__input',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': "Confirmer mot de passe",
            'class': 'signupPage__input',
        })
