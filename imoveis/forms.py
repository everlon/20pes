from django import forms
from django.core.mail.message import EmailMessage

from .models import Imovel

class ContatoForm(forms.Form):
    nome = forms.CharField(label='Nome completo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a mb-4', 'required': 'required',}))
    email = forms.EmailField(label='Seu melhor E-mail', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a mb-4', 'required': 'required',}))
    assunto = forms.CharField(label='Assunto', max_length=120, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a mb-4', 'required': 'required',}))
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea(attrs={'class': 'form-control form-control-lg mb-4', 'required': 'required', 'placeholder': 'Descreva detalhadamente sua mensagem'}))

    def send_mail(self):
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        mail = EmailMessage(
            subject = f"E-mail enviado pelo site da 20 Pés: {assunto}",
            body=conteudo,
            from_email='everlon@protonmail.com',
            to=['everlon@protonmail.com',],
            headers={'Reply-To': email}
        )
        mail.send()


class propertyNewForm(forms.ModelForm):
    nome = forms.CharField(label='Seu nome completo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a mb-4', 'required': 'required',}))
    email = forms.EmailField(label='Seu melhor e-mail para cadastro', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg form-control-a mb-4', 'required': 'required',}))

    class Meta:
        model = Imovel

        fields = (
            'nome',
            'email',
            'categoria',
            'titulo',
            'descricao',
            # 'preco',
            # 'area',
            'quartos',
            'banheiros',
            # 'suites',
            # 'vagas_garagem',
            # 'elevador',
            # 'funcionarios',
            # 'mobiliado',
            # 'churrasqueira',
            # 'piscina',
            # 'lavanderia',
            # 'portaria24',
            # 'zelador',
            # 'pet',
            # 'endereco',
            'cidade',
            'bairro',
            'uf',
            'imagem'
        )

        labels = {
            'categoria': 'Tipo da propriedade',
            'titulo': 'Frase de apresentação',
            'imagem': 'Selecione a melhor foto da propriedade',
        }

    def send_mail(self, senha, user):
        from django.urls import reverse

        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']

        conteudo = f'Nome: {nome}\nE-mail: {email}\nAssunto: Registro de usuário\nSenha temporária:{senha}\n\nAcesse o link para ATIVAR sua conta: {reverse("ativar_conta", args=[user.id])}'

        mail = EmailMessage(
            subject = f"20 Pés: Registro de usuário",
            body=conteudo,
            from_email='everlon@protonmail.com',
            to=['everlon@protonmail.com',],
            headers={'Reply-To': email}
        )
        mail.send()


class propertyNewFormAuthenticated(forms.ModelForm):

    class Meta:
        model = Imovel

        fields = (
            'categoria',
            'titulo',
            'descricao',
            'preco',
            'area',
            'quartos',
            'banheiros',
            'suites',
            'vagas_garagem',
            'elevador',
            'funcionarios',
            'mobiliado',
            'churrasqueira',
            'piscina',
            'lavanderia',
            'portaria24',
            'zelador',
            'pet',
            'endereco',
            'cidade',
            'bairro',
            'uf',
            'imagem'
        )

        labels = {
            'categoria': 'Tipo da propriedade',
            'titulo': 'Frase de apresentação',
            'imagem': 'Selecione a melhor foto da propriedade',
        }

        imagem = forms.ImageField(required=False, widget=forms.FileInput(attrs={'accept': 'image/*'}))