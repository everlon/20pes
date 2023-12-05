from django.urls import reverse_lazy
from django.contrib import messages

from django.views.generic import ListView, DetailView, TemplateView, FormView

from .forms import ContatoForm
from .models import Imovel, Categoria


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Imovel.objects.filter(active=True).order_by('?')[:6]
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context


class aboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context


class contactView(FormView):
    template_name = 'contactus.html'
    form_class = ContatoForm
    success_url = reverse_lazy('contactus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(contactView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail, favor entrar em contato')
        return super(contactView, self).form_invalid(form, *args, **kwargs)


class propertyListView(ListView):
    template_name = 'property-grid.html'
    queryset = Imovel.objects.filter(active=True)
    paginate_by = 6
    ordering = 'titulo'
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context


class propertyCatListView(ListView):
    template_name = 'property-grid.html'
    queryset = Imovel.objects.filter(active=True)
    paginate_by = 3
    context_object_name = 'imoveis'

    def get_queryset(self):
        # categoria__slug entrará no field slug do model Categoria.
        return Imovel.objects.filter(categoria__slug=self.kwargs['slug']).order_by('titulo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context


class propertyDetailView(DetailView):
    template_name = 'property-single.html'
    model = Imovel
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    queryset = Imovel.objects.filter(active=True)
    context_object_name = 'property'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.order_by('parent', 'titulo')
        return context

