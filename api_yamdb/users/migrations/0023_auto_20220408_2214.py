# Generated by Django 2.2.16 on 2022-04-08 19:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20220408_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=uuid.UUID('850e148f-4093-43da-b3b2-b436cbfe2b54'), max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]