# Generated by Django 3.1.1 on 2020-09-03 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0010_auto_20200903_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apply',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]