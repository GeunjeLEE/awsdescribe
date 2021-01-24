# Generated by Django 3.1 on 2021-01-14 11:54

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Awsenvironment',
            fields=[
                ('ae_index', models.AutoField(primary_key=True, serialize=False)),
                ('ae_name', models.CharField(max_length=30)),
                ('ae_env', models.CharField(max_length=10)),
                ('ae_id', models.CharField(max_length=15)),
                ('ae_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('user_policies', django_mysql.models.ListCharField(models.CharField(max_length=10), max_length=66, size=6)),
                ('user_groups', django_mysql.models.ListCharField(models.CharField(max_length=10), max_length=66, size=6)),
                ('user_passwdLastUesd', models.DateTimeField(null=True)),
                ('user_accesskeyLastUsed', models.DateTimeField(null=True)),
                ('user_isMFAdeviceConfigured', models.BooleanField()),
                ('user_update', models.DateTimeField(auto_now=True)),
                ('ae_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_awsdescribe.awsenvironment')),
            ],
        ),
        migrations.CreateModel(
            name='Ec2',
            fields=[
                ('ec2_id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('ec2_state', models.CharField(max_length=10)),
                ('ec2_privateip', django_mysql.models.ListCharField(models.CharField(max_length=10), max_length=66, size=6)),
                ('ec2_publicip', django_mysql.models.ListCharField(models.CharField(max_length=10), max_length=66, size=6)),
                ('ec2_tags', models.TextField()),
                ('ec2_update', models.DateTimeField(auto_now=True)),
                ('ae_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_awsdescribe.awsenvironment')),
            ],
        ),
    ]
