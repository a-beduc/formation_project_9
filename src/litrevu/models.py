from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from . import utils


class Ticket(models.Model):
    """
    Represents a ticket created by a user, containing a title, a
    description, an optional image, and a timestamp for creation.
    """
    title = models.CharField(
        max_length=128
    )
    description = models.TextField(
        max_length=2048,
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        null=True,
        blank=True
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        """
        Save the ticket instance to the database.
        If an image is provided, it is resized before saving.
        """
        if self.image:
            utils.image_resize(
                self.image,
                width=300,
                height=300
            )
        super().save(*args, **kwargs)


class Review(models.Model):
    """
    Represents a review associated with a ticket. Each review includes
    a rating, a headline, an optional body text, and a timestamp for
    creation.
    """
    ticket = models.ForeignKey(
        to=Ticket,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        # blank=True and default=0 to validate form rating at 0 when
        # user doesn't choose a rating
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        blank=True,
        default=0
    )
    headline = models.CharField(
        max_length=128
    )
    body = models.CharField(
        max_length=8192,
        blank=True
    )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    time_created = models.DateTimeField(
        auto_now_add=True
    )


class UserFollows(models.Model):
    """
    Represents the relationship where a user is following another user.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by'
    )

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)


class UserBlocks(models.Model):
    """
    Represents the relationship where a user is blocking another user.
    """
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocking'
    )
    blocked_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )

    class Meta:
        # ensures we don't get multiple UserBlocks instances
        # for unique user-user_blocked pairs
        unique_together = ('user', 'blocked_user',)
