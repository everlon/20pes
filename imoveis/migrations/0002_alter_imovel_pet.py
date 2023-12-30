# Generated by Django 4.2.4 on 2023-12-30 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='pet',
            field=models.BooleanField(choices=[(False, 'Não'), (True, 'Sim')], default=False, verbose_name='Permite animais de estimação?'),
        ),
    ]
