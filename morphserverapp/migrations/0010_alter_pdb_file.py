# Generated by Django 3.2 on 2021-04-21 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('morphserverapp', '0009_alter_pdb_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdb',
            name='file',
            field=models.FileField(null=True, upload_to='file_storage/'),
        ),
    ]
