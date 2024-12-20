# Generated by Django 5.1.2 on 2024-11-11 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('authentication', '0006_alter_group_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='users', to='auth.group'),
        ),
    ]
