# Generated by Django 2.2.16 on 2022-04-08 18:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20220408_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=uuid.UUID('44454a63-9826-4f55-9906-3cb3a1acbe67'), max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]