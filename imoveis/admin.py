from django.contrib import admin
from django.contrib.auth.models import Group

from .models import (
                Imovel,
                Imagem,
                Categoria,
                UserProfile,
            )


@admin.register(Imovel)
class ImovelAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'submitter', 'modified_at', 'active',)
    #  fields = ['nome', 'categoria',] (campos do formulário)

admin.site.register(Categoria)
admin.site.register(Imagem)
admin.site.register(UserProfile)
admin.site.unregister(Group)