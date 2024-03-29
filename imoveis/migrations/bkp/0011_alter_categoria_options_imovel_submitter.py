# Generated by Django 4.2.4 on 2023-12-16 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('imoveis', '0010_alter_imovel_churrasqueira_alter_imovel_lavanderia_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoria',
            options={'verbose_name': 'Tipo do imóvel', 'verbose_name_plural': 'Tipos de imóveis'},
        ),
        migrations.AddField(
            model_name='imovel',
            name='submitter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
