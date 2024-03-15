import random
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model, get_user
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View, ListView, DetailView, TemplateView, FormView, DeleteView, UpdateView

from .forms import ContatoForm, propertyNewForm, propertyNewFormAuthenticated, userFormDetais
from .models import Imovel, Categoria, User, UserProfile


def senha_aleatoria():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


class AtivarContaView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        user = get_user_model().objects.filter(pk=user_id).first()

        if user and not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Conta ativada com sucesso. Faça login para continuar.')
        else:
            messages.error(request, 'Ocorreu um erro ao ativar a conta. Por favor, entre em contato.')

        return redirect('painel')


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('painel')

        return super().dispatch(request, *args, **kwargs)


class PainelView(LoginRequiredMixin, ListView):
    template_name = 'painel.html'
    model = Imovel
    paginate_by = 30
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def get_queryset(self):
        return self.model.objects.filter(submitter=self.request.user.pk).order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            logout(request)
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class MyProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'myprofile.html'
    model = UserProfile
    form_class = userFormDetais
    login_url = '/login/'
    # redirect_field_name = 'myprofile'
    # success_url = reverse_lazy('myprofile')
    success_message = "Atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('myprofile', kwargs={'pk': self.kwargs['pk']})


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Imovel.objects.filter(active=True).order_by('?')[:6]
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context


class aboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context


class legalInformationView(TemplateView):
    template_name = 'legal_information.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context


class contactView(FormView):
    template_name = 'contactus.html'
    form_class = ContatoForm
    success_url = reverse_lazy('contactus')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(contactView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail, favor entrar em contato')
        return super(contactView, self).form_invalid(form, *args, **kwargs)


class propertyDevelopment(FormView):
    template_name = 'property-development.html'
    form_class = ContatoForm
    success_url = reverse_lazy('propertydevelopment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def form_valid(self, form, *args, **kwargs):
        form.send_mail()
        messages.success(self.request, 'E-mail enviado com sucesso')
        return super(contactView, self).form_valid(form, *args, **kwargs)

    def form_invalid(self, form, *args, **kwargs):
        messages.error(self.request, 'Erro ao enviar e-mail, favor entrar em contato')
        return super(contactView, self).form_invalid(form, *args, **kwargs)


class propertyNewFormView(View):
    template_name = 'property-new-form.html'
    form_class = propertyNewForm
    success_url = reverse_lazy('property-new')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('painel')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        senha=senha_aleatoria()

        if form.is_valid():
            categoria=form.cleaned_data['categoria']
            titulo=form.cleaned_data['titulo']
            descricao=form.cleaned_data['descricao']
            quartos=form.cleaned_data['quartos']
            banheiros=form.cleaned_data['banheiros']
            cidade=form.cleaned_data['cidade']
            bairro=form.cleaned_data['bairro']
            uf=form.cleaned_data['uf']
            imagem=form.cleaned_data['imagem']

            User = get_user_model()
            try:
                Usuario = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['nome'],
                    password=senha
                )
            except Exception as e:
                messages.error(self.request, 'Erro ao enviar o imóvel. Verifique os dados novamente ou o e-mail já esta cadastrado. Caso já tenha cadastrado algum imóvel anteriormente faça o Login.')
                return render(request, self.template_name, {'form': form})

            try:
                imovel = Imovel.objects.create(
                    submitter=Usuario,
                    categoria=categoria,
                    titulo=titulo,
                    descricao=descricao,
                    quartos=quartos,
                    banheiros=banheiros,
                    cidade=cidade,
                    bairro=bairro,
                    uf=uf,
                    imagem=imagem
                )
            except Exception as e:
                messages.error(self.request, 'Erro ao enviar o cadastro, favor entrar em contato.')
                return render(request, self.template_name, {'form': form})

            form.send_mail(senha, Usuario)
            messages.success(self.request, 'Cadastro enviado com sucesso. Você recebeu um e-mail com sua senha temporária. Acesse sua área de cliente pelo botão LOGIN no topo do site.')

        else:
            messages.error(self.request, 'Erro ao enviar o cadastro, verifique os dados novamente.')

        return redirect('property-new')


class propertyNewFormViewAuthenticated(LoginRequiredMixin, View):
    template_name = 'property-new-form.html'
    form_class = propertyNewFormAuthenticated
    success_url = reverse_lazy('painel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            categoria=form.cleaned_data['categoria']
            titulo=form.cleaned_data['titulo']
            descricao=form.cleaned_data['descricao']
            quartos=form.cleaned_data['quartos']
            banheiros=form.cleaned_data['banheiros']
            cidade=form.cleaned_data['cidade']
            bairro=form.cleaned_data['bairro']
            uf=form.cleaned_data['uf']
            imagem=form.cleaned_data['imagem']

            try:
                imovel = Imovel.objects.create(
                    submitter=get_user(self.request),
                    categoria=categoria,
                    titulo=titulo,
                    descricao=descricao,
                    quartos=quartos,
                    banheiros=banheiros,
                    cidade=cidade,
                    bairro=bairro,
                    uf=uf,
                    imagem=imagem,
                    active=False,
                )
                print(imovel)

            except Exception as e:
                messages.error(self.request, 'Erro ao enviar o cadastro, favor entrar em contato.')
                return render(request, self.template_name, {'form': form})

            messages.success(self.request, 'Cadastro enviado com sucesso.')

        else:
            messages.error(self.request, 'Erro ao enviar o cadastro, verifique os dados novamente.')

        return redirect('painel')


class propertyListView(ListView):
    template_name = 'property-grid.html'
    queryset = Imovel.objects.filter(active=True)
    paginate_by = 6
    ordering = 'titulo'
    context_object_name = 'imoveis'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context


class propertyCatListView(ListView):
    template_name = 'property-grid.html'
    queryset = Imovel.objects.filter(active=True)
    paginate_by = 3
    context_object_name = 'imoveis'

    def get_queryset(self):
        # categoria__slug entrará no field slug do model Categoria.
        return Imovel.objects.filter(active=True, categoria__slug=self.kwargs['slug']).order_by('titulo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
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
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        return context


class propertyDeleteView(LoginRequiredMixin, DeleteView):
    model = Imovel
    # template_name = 'imovel_confirm_delete.html'
    success_url = reverse_lazy('painel')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class propertyEditView(LoginRequiredMixin, UpdateView):
    model = Imovel
    template_name = 'property-new-form.html'
    form_class = propertyNewFormAuthenticated
    login_url = '/login/'
    redirect_field_name = 'property-edit'
    success_url = reverse_lazy('painel')
    success_message = "Atualizado com sucesso!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['property_cat'] = Categoria.objects.filter(active=True).order_by('parent', 'titulo')
        context['property_id'] = self.kwargs['pk']
        return context

    def get(self, request, *args, **kwargs):
        # print("Valor de pk:", kwargs.get('pk'))
        return self.post(request, *args, **kwargs)


def lancamentos(request):
    return render(request, 'lancamentos.html')
