# Generated by Django 5.1.4 on 2024-12-28 13:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbase', '0010_remove_article_tags_delete_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(message='Title can only contain letters, numbers, spaces, hyphens, and underscores.', regex='^[\\w\\s-]+$')]),
        ),
    ]
