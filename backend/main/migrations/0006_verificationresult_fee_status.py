# Generated by Django 5.1.5 on 2025-03-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_otpverification_alter_form_form_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificationresult',
            name='fee_status',
            field=models.IntegerField(choices=[(1, 'Pass'), (0, 'Not Pass')], default=0),
        ),
    ]
