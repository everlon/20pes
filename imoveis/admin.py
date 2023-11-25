from django.contrib import admin

from .models import (
                Imovel,
                Imagem,
                Categoria,
            )


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'modified_at', 'active',)
    #  fields = ['nome', 'categoria',] (campos do formulário)

admin.site.register(Categoria)
admin.site.register(Imagem)