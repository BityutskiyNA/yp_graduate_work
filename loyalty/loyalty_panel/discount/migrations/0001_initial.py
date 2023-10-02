# Generated by Django 4.2.4 on 2023-08-30 16:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateField(auto_now_add=True)),
                ('subscription_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.subscriptionplan')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionalCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discount_amount', models.IntegerField()),
                ('validity_period', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('subscription', models.ManyToManyField(to='discount.subscription')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('discount_amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Скидка не может быть отрицательной')])),
                ('discount_percentage', models.IntegerField(validators=[django.core.validators.MinValueValidator(0, message='Процент скидки не может быть меньше 0'), django.core.validators.MaxValueValidator(100, message='Процент скидки не может быть больше 100')])),
                ('validity_period', models.DateField(auto_now_add=True)),
                ('promo_code_type', models.CharField(choices=[('single_use', 'single-use'), ('repetitive', 'repetitive')], max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('promotional_campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.promotionalcampaign')),
            ],
        ),
        migrations.CreateModel(
            name='Discount_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateField(auto_now_add=True)),
                ('user', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('promo_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.promocode')),
                ('promotional_campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.promotionalcampaign')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='discount.subscription')),
            ],
        ),
    ]
