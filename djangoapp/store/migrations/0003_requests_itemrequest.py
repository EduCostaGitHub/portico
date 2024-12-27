# Generated by Django 5.1.4 on 2024-12-27 22:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField()),
                ('qtd_total', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('A', 'Aproved'), ('C', 'Created'), ('R', 'Reproved'), ('P', 'Pending'), ('S', 'Sent'), ('F', 'Finalized')], default='C', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
            },
        ),
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=55)),
                ('product_id', models.PositiveIntegerField()),
                ('productType', models.CharField(max_length=55)),
                ('productType_id', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('promo_price', models.FloatField(default=0)),
                ('quantity', models.PositiveIntegerField()),
                ('image', models.CharField(max_length=2000)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.requests')),
            ],
            options={
                'verbose_name': 'Item Request',
                'verbose_name_plural': 'Items of Request',
            },
        ),
    ]