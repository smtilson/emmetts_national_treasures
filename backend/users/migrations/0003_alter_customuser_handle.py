# Generated by Django 5.1.4 on 2025-03-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_friendshiprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='handle',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='handle'),
        ),
    ]
