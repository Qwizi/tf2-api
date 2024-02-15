# Generated by Django 5.0.2 on 2024-02-15 01:10

import prefix_id.field
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quality',
            fields=[
                ('id', prefix_id.field.PrefixIDField(editable=False, max_length=30, prefix='quality', primary_key=True, serialize=False, unique=True)),
                ('game_item_id', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
    ]