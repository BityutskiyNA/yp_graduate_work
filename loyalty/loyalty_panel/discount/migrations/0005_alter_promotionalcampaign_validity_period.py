# Generated by Django 4.2.4 on 2023-08-31 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0004_alter_discount_history_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotionalcampaign',
            name='validity_period',
            field=models.DateField(),
        ),
    ]
