# Generated by Django 4.2.6 on 2023-10-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_remove_userprofile_wallet_ammount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='eko_onboarding',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]