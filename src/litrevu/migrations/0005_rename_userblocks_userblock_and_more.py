# Generated by Django 5.1.7 on 2025-03-30 16:07

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('litrevu', '0004_alter_review_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserBlocks',
            new_name='UserBlock',
        ),
        migrations.RenameModel(
            old_name='UserFollows',
            new_name='UserFollow',
        ),
    ]
