# Generated by Django 4.2.8 on 2024-01-05 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_lifeblogpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifeblogpage',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
