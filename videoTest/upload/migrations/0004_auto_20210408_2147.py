# Generated by Django 3.1.7 on 2021-04-08 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20210408_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='videofile',
            field=models.FileField(null=True, upload_to='', verbose_name=''),
        ),
    ]
