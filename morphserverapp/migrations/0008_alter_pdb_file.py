# Generated by Django 3.2 on 2021-04-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morphserverapp', '0007_auto_20210421_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdb',
            name='file',
            field=models.FileField(null=True, upload_to='../morphserverapp/temp'),
        ),
    ]
