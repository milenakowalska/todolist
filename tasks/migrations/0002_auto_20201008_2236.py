# Generated by Django 3.0.2 on 2020-10-08 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='background',
            field=models.CharField(default='linear-gradient(to top, #48c6ef 0%, #6f86d6 100%)', max_length=300),
        ),
        migrations.AlterField(
            model_name='task',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
