# Generated by Django 4.2.6 on 2023-10-16 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_userprofile_is_aadhar_userprofile_is_account_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='distributer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='distributer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='super_distributer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='super_distributer', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='white_label',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='white_label', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='kyc',
            field=models.CharField(blank=True, default='pending', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]