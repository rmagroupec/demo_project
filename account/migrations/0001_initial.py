# Generated by Django 4.2.6 on 2023-10-11 17:10

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='APIManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=250)),
                ('sort_name', models.CharField(max_length=20)),
                ('url', models.CharField(max_length=200)),
                ('status', models.BooleanField()),
                ('api_key', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('optional', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('state_head', models.CharField(max_length=250)),
                ('plan_code', models.CharField(max_length=20)),
                ('state_code', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='CommissionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company_name', models.CharField(max_length=250)),
                ('sort_name', models.CharField(max_length=20)),
                ('website', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='company/')),
                ('status', models.BooleanField()),
                ('sender_id', models.CharField(max_length=200)),
                ('sms_user_id', models.CharField(max_length=200)),
                ('sms_password', models.CharField(max_length=200)),
                ('sms_uti', models.CharField(max_length=200)),
                ('smtp_url', models.CharField(max_length=200)),
                ('smtp_user_name', models.CharField(max_length=200)),
                ('smtp_password', models.CharField(max_length=200)),
                ('smtp_port', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Scheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('type', models.CharField(max_length=50)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(blank=True, max_length=50, null=True)),
                ('otp_resend', models.IntegerField(blank=True, null=True)),
                ('wallet_ammount', models.FloatField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('shop_name', models.CharField(blank=True, max_length=250, null=True)),
                ('gstin', models.CharField(blank=True, max_length=100, null=True)),
                ('gender', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('pin_code', models.CharField(blank=True, max_length=7, null=True)),
                ('pan_card', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhar_card', models.CharField(blank=True, max_length=50, null=True)),
                ('aadhar_card_front', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('aadhar_card_back', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('pan_card_pic', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('gstin_pic', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='member/')),
                ('kyc', models.CharField(blank=True, max_length=50, null=True)),
                ('callback_url', models.CharField(blank=True, max_length=250, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('reset_password', models.BooleanField(default=False)),
                ('bank_holder_name', models.CharField(blank=True, max_length=50, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_ifsc', models.CharField(blank=True, max_length=50, null=True)),
                ('app_token', models.CharField(blank=True, max_length=2000, null=True)),
                ('old_password', models.CharField(blank=True, max_length=250, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.company')),
                ('scheme', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account.scheme')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250)),
                ('re_1', models.CharField(max_length=20)),
                ('re_2', models.CharField(max_length=200)),
                ('status', models.BooleanField(default=True)),
                ('re_3', models.CharField(max_length=200)),
                ('re_4', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=200)),
                ('logo', models.URLField(blank=True, null=True)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('api_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.apimanager')),
                ('com_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.commissiontype')),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.CreateModel(
            name='Commission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=20)),
                ('white_label', models.CharField(max_length=200)),
                ('super_distributor', models.CharField(max_length=200)),
                ('distributor', models.CharField(max_length=200)),
                ('retailer', models.CharField(max_length=200)),
                ('com_type_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.commissiontype')),
                ('operator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.provider')),
                ('scheme_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.scheme')),
            ],
            options={
                'abstract': False,
                'default_permissions': ['add', 'change', 'delete', 'view'],
            },
        ),
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.role'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
