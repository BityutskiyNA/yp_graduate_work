# Generated by Django 4.2.3 on 2023-08-01 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_mailing_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing_list',
            name='subject',
            field=models.CharField(default='test', max_length=500),
            preserve_default=False,
        ),
    ]
