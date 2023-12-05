from django import forms
from django.core.mail.message import EmailMessage

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
