# Generated by Django 5.1.6 on 2025-03-08 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_fertilizer_is_public_alter_fertilizer_b_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fertilizer',
            name='n',
        ),
    ]
