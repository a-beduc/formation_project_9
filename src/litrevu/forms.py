from django import forms
from . import models
from . import widgets


class TicketForm(forms.ModelForm):
    """
    Form used to handle the creation and update of Ticket instances.
    Includes fields for title, description, and optional image upload.
    """
    class Meta:
        """
        Configuration to link between form and Ticket model, image field
        is using a custom widget.
        """
        model = models.Ticket
        fields = ['title', 'description', 'image']
        widgets = {'image': widgets.CustomFileInput(
            attrs={'class': 'formTicket__hidden'}
        )}
        labels = {
            'title': 'Titre* ',
            'description': 'Description* ',
            'image': 'Image '
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, update the widget attributes for a
        customized interface.
        """
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'formTicket__title'}
        )
        self.fields['description'].widget.attrs.update(
            {'class': 'formTicket__description'}
        )


class ReviewForm(forms.ModelForm):
    """
    Form used to handle the creation and update of Review instances.
    Includes fields for headline, body text, and rating.
    """
    class Meta:
        """
        Configuration to link between form and Review model.
        """
        model = models.Review
        fields = ['headline', 'body', 'rating']
        labels = {
            'headline': 'Titre* ',
            'rating': 'Note* ',
            'body': 'Commentaire* '
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, update the widget attributes for a
        customized interface.
        """
        super().__init__(*args, **kwargs)
        self.fields['rating'].initial = 0
        self.fields['headline'].widget.attrs.update(
            {'class': 'formReview__title'}
        )
        self.fields['rating'].widget.attrs.update(
            {'class': 'formReview__hidden'}
        )
        self.fields['body'].widget = forms.Textarea(
            attrs={'class': 'formReview__body'}
        )

    def clean_rating(self):
        """
        If rating fields hasn't been interacted with, send a 0 to the
        model.
        """
        rating = self.cleaned_data.get('rating')
        if rating in (None, ''):
            rating = 0
        return rating


class UserFollowForm(forms.Form):
    """
    Form used to handle the creation and deletion of UserFollow model.
    """
    username = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': "Nom d'utilisateur",
                   'class': 'newRelationBlock__input'}
        ),
    )


class UserBlockForm(forms.Form):
    """
    Form used to handle the creation and deletion of UserBlock model.
    """
    username = forms.CharField(
        max_length=128,
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': "Nom d'utilisateur",
                   'class': 'newRelationBlock__input'}
        ),
    )
