# Generated by Django 3.1 on 2021-11-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211106_0602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('ordering',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='ordering',
            field=models.IntegerField(default=0),
        ),
    ]
