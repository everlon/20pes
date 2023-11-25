from django.views.generic import ListView, DetailView
from .models import Imovel, Categoria


class IndexView(ListView):
    template_name = 'index.html'
    # model = Produto
    queryset = Imovel.objects.filter(active=True).order_by('?')[:6]
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        context['property']= Imovel.objects.filter(active=True)
    #     context['noticia'] = Noticia.objects.filter(active=True).order_by('-data')[:2]
    #     context['settings'] = Settings.objects.order_by('-id').first()
        return context


class propertyDetailView(DetailView):
    template_name = 'property-single.html'
    model = Imovel
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Imovel.objects.filter(active=True)
    context_object_name = 'property'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['produto_cat'] = ProdutoCategoria.objects.order_by('parent', 'titulo')
    #     context['settings'] = Settings.objects.order_by('-id').first()
    #     return context
