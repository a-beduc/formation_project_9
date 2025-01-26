from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

        def __init__(self):
            pass


class UserFollowsForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur",
                                      'class': 'newRelationBlock__input'}),
    )


class UserBlocksForm(forms.Form):
    username = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur",
                                      'class': 'newRelationBlock__input'}),
    )
