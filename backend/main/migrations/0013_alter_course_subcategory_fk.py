# Generated by Django 5.1.5 on 2025-03-22 10:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_subcategorydetails_is_pass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='subcategory_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subcategory'),
        ),
    ]
