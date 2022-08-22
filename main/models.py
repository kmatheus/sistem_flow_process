from django.db import models

import os
import re
from time import timezone
from django.forms import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager, PermissionsMixin



############### FUNÇÕES ##################

def upload_file(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000

    return "files/" + now.strftime("%Y%m%d%H%M%S") + str(milliseconds) + extension


def validar_cpf(cpf):
    cpf = "".join(re.findall("\d", str(cpf)))

    if (not cpf) or (len(cpf) < 11):
        return False

    inteiros = list(map(int, cpf))
    novo = inteiros[:9]

    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    if novo == inteiros:
        return cpf

    raise ValidationError("CPF inválido")


def validar_valores(valor):
    if float(valor) <= 0.0:
        raise ValidationError("Valor inválido")


def validar_vlr_zero(vlr):
    if float(vlr) == 0.0:
        raise ValidationError(f"O {vlr} não pode ser 0.0 !")
    return vlr


def validar_cnpj(cnpj):
    cnpj = "".join(re.findall("\d", str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    inteiros = list(map(int, cnpj))
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    if novo == inteiros:
        return cnpj

    raise ValidationError("CNPJ inválido")


# função para não capitalizar conjuções
def Cap(texto):
    """
        arg: Texto do campo
        return: Texto Capitalizado sem conjuções e texto maisculo algarismo romanos
    """
    lista_teste = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv',
                   'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxx', 'xl', 'l', 'lx', 'lxx', 'lxxx', 'xc', 'c', 'cc']

    res = texto.split()

    cont = 0
    texto = ''
    for chave, valor in enumerate(res):
        for c in lista_teste:
            if c == valor:
                cont += 1

        if cont != 0:
            texto = texto + valor.upper() + ' '
        else:
            if len(valor) != 2 and len(valor) > 1:
                texto = texto + valor.capitalize() + ' '
            else:
                texto = texto + valor + ' '

        cont = 0

    return texto


class DataCadastroMixin(models.Model):
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class UsuarioManager(BaseUserManager):
    def create_user(self, nome_log, password):
        if not nome_log:
            raise ValueError("Usuario deve ter um login")

        user = self.model(nome_log=nome_log)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nome_log, password):
        user = self.create_user(nome_log, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user



################ CLASSES DO SISTEMA ##################

class Banner(models.Model):
    img=models.CharField(max_length=300)
    alt_text=models.CharField(max_length=300)



class Usuario(AbstractBaseUser, models.Model):
    idk = models.BigAutoField(primary_key=True)
    path_img_perfil = models.ImageField(upload_to="img/pessoal/", null=True, blank=True)
    nome_log = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    is_superuser = models.BooleanField(default=False, blank=True, null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    last_ten = models.CharField(max_length=310, null=True, blank=True)
    

    objects = UsuarioManager()

    USERNAME_FIELD = "nome_log"
    REQUIRED_FIELDS = ['password', ]

    def __str__(self):
        return self.nome_log
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser



class Operador(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    nome_completo=models.CharField(max_length=80, blank=True, null=True)
    data_nascimento=models.DateField(blank=True, null=True)
    cpf=models.CharField(max_length=11, blank=True, null=True, unique=True, validators=[validar_cpf])
    funcao_operador=models.CharField(max_length=100, blank=True, null=True)
    telefone=models.CharField(max_length=11, blank=True, null=True)
    whatsapp=models.CharField(max_length=11, blank=True, null=True)
    email=models.EmailField(max_length=60, blank=True, null=True)
    endereco=models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nome_completo
    
    def clean(self):
        self.nome_completo = Cap(self.nome_completo)



class Maquinario(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    numero=models.CharField(max_length=15, blank=True, null=True, unique=True)
    nome=models.CharField(max_length=80, blank=True, null=True)
    status=models.CharField(max_length=1, blank=True, null=True)
    tipo=models.BooleanField(default=True)
    modelo=models.CharField(max_length=60, blank=True, null=True)
    valor=models.FloatField(blank=True, null=True)
    data_aquisicao=models.DateField(blank=True, null=True)
    descricao=models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.numero

    def __str__(self):
        return self.nome

    def clean(self):
        self.nome = Cap(self.nome)



class Manutencao(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    numero=models.ForeignKey(
        Maquinario,
        models.DO_NOTHING,
        db_column="numero",
        blank=True,
        null=True,
        verbose_name="Número Maquinário", related_name="numero1"
    )
    nome=models.ForeignKey(
        Maquinario,
        models.DO_NOTHING,
        db_column="nome",
        blank=True,
        null=True,
        verbose_name="Nome", related_name="nome1"
    )
    prestador_servico=models.CharField(max_length=80, blank=True, null=True)
    motivo=models.CharField(max_length=100, blank=True, null=True)
    data_envio=models.DateField(blank=True, null=True)
    provavel_retorno=models.DateField(blank=True, null=True)



class Baixa(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    numero=models.ForeignKey(
        Maquinario,
        models.DO_NOTHING,
        db_column="numero",
        blank=True,
        null=True,
        verbose_name="Número Maquinário", related_name="numero2"
    )
    nome=models.ForeignKey(
        Maquinario,
        models.DO_NOTHING,
        db_column="nome",
        blank=True,
        null=True,
        verbose_name="Nome", related_name="nome2"
    )



class Aviamento(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    codigo=models.CharField(max_length=30, blank=True, null=True, unique=True)
    produto=models.CharField(max_length=60, blank=True, null=True)
    nome=models.CharField(max_length=80, blank=True, null=True)
    categoria=models.CharField(max_length=60, blank=True, null=True)
    fornecedor=models.CharField(max_length=80, blank=True, null=True)
    marca=models.CharField(max_length=80, blank=True, null=True)
    valor=models.FloatField(blank=True, null=True)
    data_aquisicao=models.DateField(blank=True, null=True)
    quantidade=models.IntegerField(blank=True, null=True)
    descricao=models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.nome

    def clean(self):
        self.nome = Cap(self.nome)
        self.fornecedor = Cap(self.fornecedor)
        self.marca = Cap(self.marca)



class Processo(models.Model):
    idk=models.BigAutoField(primary_key=True, blank=False, null=False)
    nome=models.CharField(max_length=80, blank=True, null=True)
    tempo_execucao=models.TimeField(blank=True, null=True)
    operador_alocado=models.ForeignKey(
        Operador,
        on_delete=models.CASCADE,
        db_column="operador_alocado",
        blank=True,
        null=True,
        verbose_name="Operador Alocado", related_name="nome_completo1"
    )
    aviamento_utilizado=models.ForeignKey(
        Aviamento, 
        on_delete=models.CASCADE,
        db_column="aviamento_utilizado",
        blank=True,
        null=True,
        verbose_name="Aviamento Utilizado", related_name="nome1"
    )
    maquinario_alocado=models.ForeignKey(
        Maquinario,
        models.DO_NOTHING,
        db_column="maquinario_alocado",
        blank=True,
        null=True,
        verbose_name="Maquinário Alocado", related_name="nome3"
    )

    def clean(self):
        self.nome = Cap(self.nome)