import uuid
from django.db import models
from stdimage.models import StdImageField
from django.contrib.auth.models import User

#  SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify


UF_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)


def get_file_path(_instance, filename):
    #  Criar nome aleatório para os arquivos.
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename


class Base(models.Model):
    active = models.BooleanField('Situação', default=True)
    created_at = models.DateField('Data de Criação', auto_now_add=True)
    modified_at = models.DateField('Data de Atualização', auto_now=True, blank=True)
    slug = models.SlugField('Slug', max_length=255, blank=True, null=True, editable=False, unique=True)

    class Meta:
        abstract = True


class Categoria(Base):
    titulo = models.CharField(max_length=150, db_index=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tipo do imóvel'
        verbose_name_plural = 'Tipos de imóveis'

    def __str__(self):
        full_path = [self.titulo]
        return '/'.join(full_path[::-1])


class Imagem(Base):
    titulo = models.CharField(max_length=50)
    descricao = models.TextField('Descrição', max_length=100, blank=True)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 1024, 'height': 1024}}, blank=True)

    class Meta:
        verbose_name = 'Imagem'
        verbose_name_plural = 'Galeria de imagens'

    def __str__(self):
        return self.titulo


class Imovel(Base):
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField('Título', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2, blank=True, null=True)
    imagem = StdImageField('Imagem', upload_to=get_file_path, variations={'thumb': {'width': 480, 'height': 480, 'crop': True}}, blank=True)
    descricao = models.TextField('Descrição', max_length=1200, blank=True)  # HTMLField ?
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    endereco = models.CharField('Endereço', max_length=150, blank=True, null=True)
    cidade = models.CharField('Cidade', max_length=150, blank=True, null=True)
    bairro = models.CharField('Bairro', max_length=150, blank=True, null=True)
    uf = models.CharField('Estado', max_length=2, choices=UF_CHOICES, blank=True, null=True)
    area = models.PositiveSmallIntegerField('Área', null=True, default='1')
    quartos = models.PositiveSmallIntegerField('Quartos', null=True, default='1')
    banheiros = models.PositiveSmallIntegerField('Banheiros', null=True, default='1')
    suites = models.PositiveSmallIntegerField('Suítes', null=True, default='0')
    vagas_garagem = models.PositiveSmallIntegerField('Vagas na garagem', null=True, default='1')
    elevador = models.PositiveSmallIntegerField('Elevador', null=True, default='0')
    galeria_imagens = models.ManyToManyField(Imagem, blank=True)
    video_yt = models.TextField('Video', max_length=1200, blank=True)  # HTMLField ?
    google_map = models.TextField('Mapa', max_length=1200, blank=True)  # HTMLField ?

    funcionarios = models.PositiveSmallIntegerField('Funcionários', null=True, default='0')
    mobiliado = models.BooleanField('Mobiliado', default=False)
    churrasqueira = models.BooleanField('Churrasqueira', default=False)
    piscina = models.BooleanField('Piscina', default=False)
    lavanderia = models.BooleanField('Lavanderia', default=False)
    portaria24 = models.BooleanField('Portaria 24 hrs', default=False)
    zelador = models.BooleanField('Zelador', default=False)
    pet = models.BooleanField('Pode pet?', default=False)

    class Meta:
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'

    def __str__(self):
        return self.titulo


#  SIGNALS: Criar URLs amigáveis / Slugs
def imovel_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.titulo)

def categ_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.titulo)

signals.pre_save.connect(imovel_pre_save, sender=Imovel)
signals.pre_save.connect(categ_pre_save, sender=Categoria)
