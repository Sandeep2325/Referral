# Generated by Django 5.0.4 on 2024-04-07 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referral_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
