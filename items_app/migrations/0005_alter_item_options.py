# Generated by Django 5.1.5 on 2025-01-16 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items_app', '0004_alter_category_options_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('name',)},
        ),
    ]
