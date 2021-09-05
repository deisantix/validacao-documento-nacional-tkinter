from email_validator import validate_email, EmailNotValidError
from validation_classes.valida_doc_interface import IByteBank
from validate_docbr import CPF, CNPJ
from datetime import date, datetime
import simplejson.errors
import requests
import re

"""
classe que usa a biblioteca datetime para
salvar o momento de cadastro e 
a data de nascimento do usuário
"""


class DataByteBank(IByteBank):
    def __init__(self, data_entrada=""):
        data_entrada = str(data_entrada)

        self._momento_cadastro = datetime.today()

        self.valido = self.eh_valido(data_entrada)
        if self.valido[0]:
            self._data_nascimento = self.valido[1]
        else:
            self._data_nascimento = None

    @property
    def data_nascimento(self):
        return self._data_nascimento

    """
    se coloca data de nascimento
    que é validada e retorna uma tupla 
    com o status, e mensagem de erro caso preciso
    """
    @staticmethod
    def eh_valido(data_nascimento_para_validar):
        data_nascimento_para_validar = str(data_nascimento_para_validar)

        padrao_data = re.compile("(\d{2})/?(\d{2})/?(\d{4})")
        verificar_data = padrao_data.match(data_nascimento_para_validar)

        if not verificar_data:
            return False, "Insira a data no formato DD/MM/AAAA"

        try:
            particoes_data = verificar_data.groups()

            day = int(particoes_data[0])
            month = int(particoes_data[1])
            year = int(particoes_data[2])

            if year >= datetime.today().year:
                return False, "Data inválida"

            data_nascimento = date(year, month, day)
            data_nascimento = data_nascimento.strftime('%d/%m/%Y')

            return True, data_nascimento

        except ValueError:
            return False, "Data inválida"

    """
    devolve mês do cadastro por extenso
    """
    def devolver_mes_por_extenso(self):
        meses_do_ano = ('janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho',
                        'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro')

        return meses_do_ano[self._momento_cadastro.month - 1]

    """
    devolve dia da semana do cadastro por extenso
    """
    def devolver_dia_por_extenso(self):
        dias_da_semana = ('Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo')

        return dias_da_semana[self._momento_cadastro.weekday()]

    def _mascara(self):
        return self._momento_cadastro.strftime(f'{self.devolver_dia_por_extenso()}, %d de '
                                               f'{self.devolver_mes_por_extenso()} de %Y %H:%M')


"""
valida a syntax do email inserido
### não verifica se existe de fato
"""


class EmailByteBank(IByteBank):
    def __init__(self, email_inicial=""):
        email_inicial = str(email_inicial)
        self.valido = self.eh_valido(email_inicial)

        if self.valido[0]:
            self.email = email_inicial
        else:
            self.email = None

    """
    usa biblioteca instalada no pypi para validar a syntaxe do email
    """
    @staticmethod
    def eh_valido(email_para_validar):
        try:
            validate_email(email_para_validar)

        except EmailNotValidError:
            return False, "Email inválido"

        return True, ""

    def _mascara(self):
        if self.email:
            return self.email
        else:
            return self.valido[1]


"""
valida CPF com biblioteca instalada no pypi
"""


class CPFByteBank(IByteBank):
    def __init__(self, cpf_entrada=""):
        cpf_entrada = str(cpf_entrada)
        self.valido = self.eh_valido(cpf_entrada)

        if self.valido[0]:
            self._cpf = cpf_entrada
        else:
            self._cpf = None

    """
    usa RegEx para validar syntaxe do CPF
    """

    @staticmethod
    def eh_valido(cpf_para_validar):
        cpf_para_validar = str(cpf_para_validar)

        cpf_padrao = re.compile("\d{3}\.?\d{3}\.?\d{3}-?\d{2}")
        verifica_cpf = cpf_padrao.match(cpf_para_validar)

        if not verifica_cpf:
            return False, "CPF inválido"

        validador = CPF()
        if not validador.validate(cpf_para_validar):
            return False, "CPF inválido"

        return True, ""

    def _mascara(self):
        if self._cpf:
            cpf_padrao = re.compile("(\d{3})\.?(\d{3})\.?(\d{3})-?(\d{2})")
            particoes_cpf = cpf_padrao.match(self._cpf).groups()

            return f'{particoes_cpf[0]}.{particoes_cpf[1]}.{particoes_cpf[2]}-{particoes_cpf[3]}'
        else:
            return self.valido[1]


"""
classe identica a classe do CPF, porém para CNPJ
"""


class CNPJByteBank(IByteBank):
    def __init__(self, cnpj_entrada):
        cnpj_entrada = str(cnpj_entrada)
        self.valido = self.eh_valido(cnpj_entrada)

        if self.valido[0]:
            self._cnpj = cnpj_entrada
        else:
            self._cnpj = None

    @staticmethod
    def eh_valido(cnpj_para_validar):
        cnpj_para_validar = str(cnpj_para_validar)

        cpf_padrao = re.compile("\d{2}\.?\d{3}\.?\d{3}/?0001-?\d{2}")
        verifica_cnpj = cpf_padrao.match(cnpj_para_validar)

        if not verifica_cnpj:
            return False, 'CNPJ inválido'

        validador = CNPJ()
        if not validador.validate(cnpj_para_validar):
            return False, 'CNPJ inválido'

        return True, ""

    def _mascara(self):
        if self._cnpj:
            cnpj_padrao = re.compile("(\d{2})\.?(\d{3})\.?(\d{3})/?(0001)-?(\d{2})")
            particoes_cnpj = cnpj_padrao.match(self._cnpj).groups()

            return f'{particoes_cnpj[0]}.{particoes_cnpj[1]}.{particoes_cnpj[2]}/{particoes_cnpj[3]}-{particoes_cnpj[4]}'
        else:
            return self.valido[1]


"""
valida telefone celular nacional
### apenas nacional
### telefone fixo não incluso
"""


class TelefoneByteBank(IByteBank):
    def __init__(self, telefone=""):
        telefone = str(telefone)
        self.valido = self.eh_valido(telefone)

        if self.valido[0]:
            self.numero = telefone
            self.ddd = self.valido[1]
        else:
            self.numero = None
            self.ddd = None


    """
    valida o número verificando se o ddi é nacional, caso não seja não será considerado válido
    verifica se o ddi é valido por meio de uma lista de ddis dos estados brasileiros
    e verifica se a quantidade de números está correta
    """
    @staticmethod
    def eh_valido(numero_para_validar):
        numero_para_validar = str(numero_para_validar)

        pais_padrao = "\+\d{2}\d?"
        ddd_padrao = "\(?(\d{2})\)?"
        numero_padrao = re.compile("(\+55 ?)?\(?\d{2}\)? ?9\d{4}-?\d{4}")

        verificar_numero = re.match(numero_padrao, numero_para_validar)
        if not verificar_numero:
            return False, 'Número inválido'

        verificar_pais = re.search(pais_padrao, numero_para_validar)
        if verificar_pais and "+55" not in numero_para_validar:
            return False, "Insira um número nacional"
        elif verificar_numero and "+55" in numero_para_validar:
            numero_para_validar = numero_para_validar[3:].strip()

        ddd = numero_para_validar[:-9].strip()

        verificar_ddd = re.search(ddd_padrao, ddd).group(1)
        ddd = verificar_ddd

        ddds_do_brasil = devolver_lista_de_ddd()
        if ddd not in ddds_do_brasil:
            return False, 'ddd inválido'

        return True, ddd

    def _mascara(self):
        if self.numero:
            numero_padrao = re.compile('\(?(\d{2})\)? ?(9\d{4})-?(\d{4})')
            particoes_do_numero = numero_padrao.search(self.numero).groups()

            return f'({particoes_do_numero[0]}) {particoes_do_numero[1]}-{particoes_do_numero[2]}'
        else:
            return self.valido[1]


"""
faz request em site para pegar lista em html com ddds brasileiros
"""


def procurar_ddd():
    site_ddd = 'https://totalip.com.br/quais-os-ddds-de-cada-estado-do-brasil/'  # especificando a url
    page = requests.get(site_ddd)  # fazer request da pagina de web
    analise_html = page.text  # retornar o conteudo da pagina (mais especificamente colocando o conteudo na variavel)

    lista_de_ddd = re.findall('&#8211; [\w\s]* (\([\d\s,e]*\))', analise_html)

    return lista_de_ddd


"""
torna a lista de ddds, coletada na função acima, usável
"""


def devolver_lista_de_ddd():
    lista_de_ddd = procurar_ddd()

    lista_de_codigos_ddd = []
    for estado in lista_de_ddd:
        re_find = re.findall('\d{2}', estado)

        for ddd in re_find:
            lista_de_codigos_ddd.append(ddd)

    return sorted(lista_de_codigos_ddd)


"""
classe para validação de CEP
"""


class CEPByteBank(IByteBank):
    def __init__(self, documento=""):
        documento = str(documento)
        self.valido = self.eh_valido(documento)

        if self.valido[0]:
            self._cep = documento
            self._endereco = self.valido[1]
        else:
            self._cep = None

    @property
    def endereco(self):
        return self._endereco

    """
    valida cep por meio da syntaxe usando RegEx
    e caso passe no primeiro teste, procura o cep usando uma API
    retornando uma tupla com bool e dicionario caso seja valido
    """

    @staticmethod
    def eh_valido(cep_para_validar):
        cep_para_validar = str(cep_para_validar)

        padrao_cep = "\d{5}-?\d{3}"
        validar_cep = re.match(padrao_cep, cep_para_validar)

        if not validar_cep:
            return False, 'CEP inválido'

        api_cep = consultar_cep_via_api(cep_para_validar)
        if api_cep.get('erro', 0):
            return False, 'CEP não encontrado no banco de dados'

        return True, api_cep

    def _mascara(self):
        if self._cep:
            padrao_cep = re.compile('(\d{5})-?(\d{3})')
            particoes_cep = padrao_cep.search(self._cep).groups()

            return f'{particoes_cep[0]}-{particoes_cep[1]}'
        else:
            return self.valido[1]


"""
consulta a api para pegar o cep
"""


def consultar_cep_via_api(cep_para_procurar):
    try:
        page = requests.get(f'https://viacep.com.br/ws/{cep_para_procurar}/json/')
        analisa_json = page.json()

        return analisa_json

    except simplejson.errors.JSONDecodeError:
        return {'erro': True}


"""
função que usa uma api para retornar um dicionario com todos
os estados do brasil e sua siglas e id's
"""


def procurar_estados():
    site_estados = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/'
    page = requests.get(site_estados)
    analise_json = page.json()

    estados_brasil = {}
    estados_por_id = {}
    for item in analise_json:
        estados_brasil[item["nome"].upper()] = item["sigla"]
        estados_por_id[item["nome"].upper()] = item["id"]

    return estados_brasil, estados_por_id


"""
busca a mesma api anterior para verificar
os municípios do estado inserido anteriormente
"""


def procurar_municipios_por_distrito(estado):
    estado = str(estado).upper()
    estados_por_sigla, estados_por_id = procurar_estados()

    cidades = []
    site_municipios = ""
    try:
        site_municipios = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estados_por_id[estado]}/municipios"
    except KeyError:
        pass

    try:
        for nome, sigla in estados_por_sigla.items():
            estado_certo = nome

            if estados_por_sigla[estado_certo] == estado:
                estado = estado_certo

        site_municipios = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{estados_por_id[estado]}/municipios"

    except KeyError:
        cidades.append("erro")

    finally:
        page = requests.get(site_municipios)
        analise_json = page.json()

        for item in analise_json:
            cidades.append(item["nome"].upper())

        return cidades
