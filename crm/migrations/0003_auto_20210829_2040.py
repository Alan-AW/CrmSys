# Generated by Django 3.2.5 on 2021-08-29 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20210829_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': '项目'},
        ),
        migrations.AlterModelTable(
            name='project',
            table='project',
        ),
    ]