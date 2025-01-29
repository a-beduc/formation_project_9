from django import forms
from . import models
from . import widgets


class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'image': widgets.CustomFileInput(attrs={'class': 'formTicket__hidden'}), }
        labels = {'title': 'Titre* ', 'description': 'Description* ', 'image': 'Image '}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'formTicket__title'})
        self.fields['description'].widget.attrs.update({'class': 'formTicket__description'})


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
