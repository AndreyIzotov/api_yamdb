# Generated by Django 2.2.16 on 2022-03-31 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_confirmation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verification_code',
            field=models.CharField(max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]