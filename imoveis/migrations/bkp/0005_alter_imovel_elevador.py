# Generated by Django 4.2.7 on 2023-11-18 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imoveis', '0004_imovel_banheiros_imovel_elevador_imovel_quartos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='elevador',
            field=models.PositiveSmallIntegerField(default='1', verbose_name='Elevador'),
        ),
    ]