# Generated by Django 4.2.6 on 2023-10-14 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_userprofile_eko_onboarding'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='dob',
            field=models.CharField(blank=True, default='1990-10-12', max_length=250, null=True),
        ),
    ]