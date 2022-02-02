# Generated by Django 3.2.7 on 2022-01-30 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
        ('article', '0001_schema__initial_model_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='region_list', to='author.author'),
            preserve_default=False,
        ),
    ]
