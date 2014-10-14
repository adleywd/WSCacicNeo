import requests
import json
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from .models import (
    DBSession,
    SistemaOperacional,
    )
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase
from wscacicneo.model.reports import Reports
from wscacicneo.model.notify import Notify
from wscacicneo.model.notify import NotifyBase
from wscacicneo.model import coleta_manual
from wscacicneo.model.reports import Reports

from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv
from liblightbase.lbrest.document import DocumentREST
from pyramid.view import forbidden_view_config

from pyramid.security import (
    remember,
    forget,
    )

engine = create_engine('postgresql://rest:rest@localhost/cacic')
REST_URL = 'http://api.brlight.net/api'

Session = sessionmaker(bind=engine)
session = Session()

# Views de configuração
@view_config(route_name='blankmaster', renderer='templates/blankmaster.pt')
def blankmaster(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='master', renderer='templates/master.pt')
def master(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='root')
def root(request):
    return {'project': 'WSCacicNeo'}

# Views básicas
@view_config(route_name='home', renderer='templates/home.pt')
def home(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='error', renderer='templates/error.pt')
def error(request):
    return {'project': 'WSCacicNeo'}

# Lista de Notificação
@view_config(route_name='list_notify', renderer='templates/list_notify.pt')
def list_notify(request):
    notify_obj = Notify(
        orgao = 'deasdsd',
        id_coleta = 'saudhasd',
        notify = 'sadsad',
        status = 'sadasd'
    )
    reg = notify_obj.search_list_notify()
    doc = reg.results
    return {'doc': doc}


@view_config(route_name='notify', renderer='templates/notify_coleta.pt')
def notify(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='post_notify')
def post_notify(request):
    requests = request.params
    notify_obj = Notify(
        orgao = requests['orgao'],
        id_coleta = requests['id_coleta'],
        notify = requests['notify'],
        status = requests['status']
    )
    results = notify_obj.create_notify()
    return Response(str(results))

# Views de Orgão
@view_config(route_name='orgao', renderer='templates/orgao.pt')
def orgao(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='listorgao', renderer='templates/list_orgao.pt')
def listorgao(request):
    orgao_obj = Orgao(
        nome = 'sahuds',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    return {'orgao_doc': search.results}

@view_config(route_name='editorgao', renderer='templates/editarorgao.pt')
def editorgao(request):
    sigla = request.matchdict['sigla']
    orgao_obj = Orgao(
        nome = 'asdsad',
        cargo = 'cargo',
        coleta = '4h',
        sigla = sigla,
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_orgao(sigla)
    return {
        'nome' : search.results[0].nome,
        'cargo' : search.results[0].cargo,
        'coleta' : search.results[0].coleta,
        'sigla' : search.results[0].sigla,
        'endereco' : search.results[0].endereco,
        'email' : search.results[0].email,
        'telefone' : search.results[0].telefone,
        'url' : search.results[0].url
    }

@view_config(route_name='post_orgao')
def post_orgao(request):
    """
    Post doc órgãos
    """
    rest_url = REST_URL
    orgaobase = OrgaoBase().lbbase
    doc = request.params
    orgao_obj = Orgao(
        nome = doc['nome'],
        cargo = doc['gestor'],
        coleta = doc['coleta'],
        sigla = doc['sigla'],
        endereco = doc['end'],
        email = doc['email'],
        telefone = doc['telefone'],
        url = doc['url']
    )

    id_doc = orgao_obj.create_orgao()

    return Response(str(id_doc))

@view_config(route_name='put_orgao')
def put_orgao(request):
    """
    Edita um doc apartir do id
    """
    params = request.params
    sigla = params['id']
    orgao_obj = Orgao(
        nome = params['nome'],
        cargo = params['gestor'],
        coleta = params['coleta'],
        sigla = params['sigla'],
        endereco = params['end'],
        email = params['email'],
        telefone = params['telefone'],
        url = params['url']
    )
    orgao = {
        'nome' : params['nome'],
        'cargo' : params['gestor'],
        'coleta' : params['coleta'],
        'sigla' : params['sigla'],
        'endereco' : params['end'],
        'email' : params['email'],
        'telefone' : params['telefone'],
        'url' : params['url']
    }
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(orgao)
    edit = orgao_obj.edit_orgao(id, doc)

    return Response(edit)

@view_config(route_name='delete_orgao')
def delete_orgao(request):
    """
    Deleta doc apartir do id
    """
    doc = request.params
    sigla = request.matchdict['sigla']
    orgao_obj = Orgao(
        nome = 'asdasd',
        cargo = 'asdasdasd',
        coleta = 'asdasdasd',
        sigla = 'asdasdas',
        endereco = 'asdsad',
        email = 'asdsad',
        telefone = 'sadasd',
        url = 'sadasd'
    )
    search = orgao_obj.search_orgao(sigla)
    id = search.results[0]._metadata.id_doc
    delete = orgao_obj.delete_orgao(id)

    return Response(delete)

# Views de Favoritos
@view_config(route_name='favoritos', renderer='templates/favoritos.pt')
def favoritos(request):
    matricula = request.matchdict['matricula']
    user_obj = User(
        nome = 'base',
        matricula = matricula,
        email = 'base@gov.br',
        orgao = 'orgao',
        telefone = 'telefone',
        cargo = 'cargo',
        setor = 'setor',
        permissao = 'Gestor',
        favoritos = ['asdsadasd', 'asdasdasd'],
        senha = 'senha'
    )
    search = user_obj.search_user(matricula)
    favoritos = search.results[0].favoritos
    return {
        'favoritos': search.results[0].favoritos,
        'itens': search.results[0].itens,
        'nome' : search.results[0].nome,
        'matricula' : search.results[0].matricula,
        'email' : search.results[0].email,
        'orgao' : search.results[0].orgao,
        'telefone' : search.results[0].telefone,
        'cargo' : search.results[0].cargo,
        'setor' : search.results[0].setor,
        'permissao' : search.results[0].permissao,
        'senha' : search.results[0].senha
    }

@view_config(route_name='edit_favoritos')
def edit_favoritos(request):
    """
    Editar do Favoritos
    """
    documento = json.loads(request.params['documento'])
    matricula = documento['matricola']
    user_obj = User(
        nome = documento['nome'],
        matricula = documento['matricula'],
        email = documento['email'],
        orgao = documento['orgao'],
        telefone = documento['telefone'],
        cargo = documento['cargo'],
        setor = documento['setor'],
        permissao = documento['permissao'],
        senha = documento['senha']
    )
    user = {
        'nome' : documento['nome'],
        'matricula' : documento['matricula'],
        'email' : documento['email'],
        'orgao' : documento['orgao'],
        'telefone' : documento['telefone'],
        'cargo' : documento['cargo'],
        'setor' : documento['setor'],
        'permissao' : documento['permissao'],
        'senha' : documento['senha'],
        'itens': documento['itens'],
        'favoritos': documento['favoritos']
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    doc = json.dumps(user)
    edit = user_obj.edit_user(id, doc)

    return Response(edit)

# Reports
@view_config(route_name='create_orgao')
def create_base(request):
    nm_orgao = request.matchdict['nm_orgao']
    coletaManualBase = coleta_manual.ColetaManualBase(nm_orgao)
    lbbase = coletaManualBase.lbbase
    retorno = coletaManualBase.create_base()

    return HTTPFound(request.route_url('root') + 'orgao/lista')

@view_config(route_name='conf_report', renderer='templates/conf_report.pt')
def conf_report(request):
    orgao_obj = Orgao(
        nome = 'sahuds',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    return {'orgao_doc': search.results}

@view_config(route_name='report_itens', renderer='templates/report.pt')
def report_itens(request):
    nm_orgao = request.matchdict['nm_orgao']
    attr = request.matchdict['attr']
    child = request.matchdict['child']
    data = Reports(nm_orgao).count_attribute(attr, child)
    return {'data': data }

# Users

@view_config(route_name='user', renderer='templates/user.pt', permission='edit')
def user(request):
    return {'project': 'WSCacicNeo'}

@view_config(route_name='post_user')
def post_user(request):
    """
    Post doc users
    """
    rest_url = REST_URL
    userbase = UserBase().lbbase
    doc = request.params
    email_user = doc['email']
    email_is_institucional = Utils.verifica_email_institucional(email_user)
    if(email_is_institucional):
        document = doc['favoritos']
        favoritos = [document]
        itens = [doc['lista_orgao'], doc['cadastro_orgao'], doc['lista_user'], doc['cadastro_user'], doc['coleta'], doc['notify']]
        user_obj = User(
            nome = doc['nome'],
            matricula = doc['matricula'],
            email = doc['email'],
            orgao = doc['orgao'],
            telefone = doc['telefone'],
            cargo = doc['cargo'],
            setor = doc['setor'],
            permissao = doc['permissao'],
            senha = doc['senha'],
            favoritos = favoritos,
            itens = itens
        )
        id_doc = user_obj.create_user()

        return Response(str(id_doc))
    else:
        return {"emailerrado":"emailerrado"}

@view_config(route_name='edituser', renderer='templates/editaruser.pt', permission="edit")
def edituser(request):
    matricula = request.matchdict['matricula']
    user_obj = User(
        nome = 'base',
        matricula = matricula,
        email = 'base@gov.br',
        orgao = 'orgao',
        telefone = 'telefone',
        cargo = 'cargo',
        setor = 'setor',
        permissao = 'Gestor',
        senha = 'senha'
    )
    search = user_obj.search_user(matricula)
    return {
        'nome' : search.results[0].nome,
        'matricula' : search.results[0].matricula,
        'email' : search.results[0].email,
        'orgao' : search.results[0].orgao,
        'telefone' : search.results[0].telefone,
        'cargo' : search.results[0].cargo,
        'setor' : search.results[0].setor,
        'permissao' : search.results[0].permissao,
        'senha' : search.results[0].senha
    }

@view_config(route_name='put_user')
def put_user(request):
    """
    Edita um doc de user apartir do id
    """
    params = request.params
    matricula = params['url']
    user_obj = User(
        nome = params['nome'],
        matricula = params['matricula'],
        email = params['email'],
        orgao = params['orgao'],
        telefone = params['telefone'],
        cargo = params['cargo'],
        setor = params['setor'],
        permissao = params['permissao'],
        senha = params['senha']
    )
    user = {
        'nome' : params['nome'],
        'matricula' : params['matricula'],
        'email' : params['email'],
        'orgao' : params['orgao'],
        'telefone' : params['telefone'],
        'cargo' : params['cargo'],
        'setor' : params['setor'],
        'permissao' : params['permissao'],
        'senha' : params['senha']
    }
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    email_user = params['email']
    email_is_institucional = Utils.verifica_email_institucional(email_user)
    if(email_is_institucional):
        doc = json.dumps(user)
        edit = user_obj.edit_user(id, doc)
        return Response(edit)

    else:
        return { }

@view_config(route_name='listuser', renderer='templates/list_user.pt', permission="view")
def listuser(request):
    user_obj = User(
        nome = 'asdasd',
        matricula = 'asdasd',
        email = 'asdsad',
        orgao = 'asdsad',
        telefone = 'sdasd',
        cargo = 'asdasdasd',
        setor = 'asdasd',
        permissao = 'asdasd',
        senha = 'sadasdasd',
        favoritos = ['asdasdasdasd']
    )
    search = user_obj.search_list_users()
    return {'user_doc': search.results}

@view_config(route_name='delete_user')
def delete_user(request):
    """
    Deleta doc apartir do id
    """
    doc = request.params
    matricula = request.matchdict['matricula']
    user_obj = User(
        nome = 'asdasd',
        matricula = 'asdasd',
        email = 'asdsad',
        orgao = 'asdsad',
        telefone = 'sdasd',
        cargo = 'asdasdasd',
        setor = 'asdasd',
        permissao = 'asdasd',
        senha = 'sadasdasd',
        favoritos = ['asdasdasdasd']
    )
    search = user_obj.search_user(matricula)
    id = search.results[0]._metadata.id_doc
    delete = user_obj.delete_user(id)
    return Response(delete)

# Autenticação
@view_config(route_name='login', renderer='templates/login.pt')
@forbidden_view_config(renderer='templates/login.pt')
def login(request):
    user_obj = User(
        nome = 'asdasd',
        matricula = 'asdasd',
        email = 'asdsad',
        orgao = 'asdsad',
        telefone = 'sdasd',
        cargo = 'asdasdasd',
        setor = 'asdasd',
        permissao = 'asdasd',
        senha = 'sadasdasd',
        favoritos = ['asdasdasdasd']
    )
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = request.route_url('root') + 'home' # never use the login form itself as came_from
    came_from = request.params.get('came_from', referrer)
    message = ''
    email = ''
    senha = ''
    is_visible = 'none'
    if 'form.submitted' in request.params:
        email = request.params['email']
        senha = request.params['senha']
        try:
            usuario = user_obj.search_user_by_email(email)
            if usuario.results[0].senha == senha:
                headers = remember(request, email)
                return HTTPFound(location = came_from,
                                 headers = headers)
            is_visible = "block"
            message = 'E-mail ou senha incorretos'
        except:
            is_visible = "block"
            message = 'E-mail ou senha incorretos'

    return dict(
        message = message,
        url = request.application_url + '/login',
        came_from = came_from,
        email = email,
        senha = senha,
        is_visible = is_visible,
        )

@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location = request.route_url('login'),
                     headers = headers)

# Coleta
@view_config(route_name='cadastro_coleta', renderer='templates/cadastro_coleta.pt')
def cadastro_coleta(request):
    orgao_obj = Orgao(
        nome = 'teste',
        cargo = 'cargo',
        coleta = '4h',
        sigla = 'MPOG',
        endereco = 'Esplanada bloco C',
        email = 'admin@planemaneto.gov.br',
        telefone = '(61) 2025-4117',
        url = 'http://api.brlight.net/api'
    )
    search = orgao_obj.search_list_orgaos()
    return {'orgao_doc': search.results}


@view_config(route_name='post_coleta_manual')
def post_coleta_manual(request):
    """
    Post doc ColetaManual
    """
    document = request.params
    nm_base = document['orgao']
    data_coleta = document['data_coleta'],
    softwarelist = document['softwarelist'],
    win32_processor_manufacturer = document['win32_processor_manufacturer'],
    win32_processor_numberoflogicalprocessors = document['win32_processor_numberoflogicalprocessors'],
    win32_processor_caption = document['win32_processor_caption'],
    operatingsystem_version = document['operatingsystem_version'],
    operatingsystem_installdate = document['operatingsystem_installdate'],
    operatingsystem_caption = document['operatingsystem_caption'],
    win32_bios_manufacturer = document['win32_bios_manufacturer']

    coleta_dict= { 
        "data_coleta" : data_coleta,
        "softwarelist" : [softwarelist],
        "win32_processor": {
            "win32_processor_manufacturer": win32_processor_manufacturer,
            "win32_processor_numberoflogicalprocessors": win32_processor_numberoflogicalprocessors,
            "win32_processor_caption" : win32_processor_caption
        },
        "operatingsystem": {
            "operatingsystem_version": operatingsystem_version,
            "operatingsystem_installdate": operatingsystem_installdate,
            "operatingsystem_caption" : operatingsystem_caption
        },
        "win32_bios": {
            "win32_bios_manufacturer": win32_bios_manufacturer
        }
    }
    id_doc = Reports(nm_base).create_coleta(coleta_dict)
    return Response(str(id_coleta))
