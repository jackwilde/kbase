# Generated by Django 5.1.2 on 2024-11-21 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbase', '0009_article_groups_with_edit_article_groups_with_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
