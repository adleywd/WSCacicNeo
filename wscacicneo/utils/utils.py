#!/usr/env python
# -*- coding: utf-8 -*-
import requests
import json
import unicodedata
import hashlib
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from wscacicneo.model.user import User
from wscacicneo.model.user import UserBase
from wscacicneo.model.base_reports import ReportsBase
from wscacicneo.model.config_reports import ConfReports
from wscacicneo.model.coleta_manual import ColetaManualBase
from wscacicneo.model.reports import Reports
from wscacicneo.model.atividade import Atividade
from wscacicneo.model.atividade import AtividadeBase
from wscacicneo.model.descriptions import DescriptionsBase
from wscacicneo.model.descriptions import Desc
from wscacicneo import config

class Utils:

    def __init__(self):
        pass

    def to_url(*args):
        return '/'.join(list(args))

    # Retorna verdadeiro para um email passado no qual contenha um e-mail institucional
    # no caso, quando o e-mail tiver gov.br
    def verifica_email_institucional(email):
        if "gov.br" in email:
            return True
        else:
            return False

    # Retorna uma string sem caracteres especiais(sem espaço e acentos).
    def format_name(data):
        return ''.join(x for x in unicodedata.normalize('NFKD', data) if \
        unicodedata.category(x)[0] == 'L').lower()

    # Retorna um hex de um objeto hash, com uma senha encryptada
    def hash_password(password):
        hash_object = hashlib.md5(password.encode("utf-8"))
        return hash_object.hexdigest()

    def create_user_obj():
        user_obj = User(
            nome = 'usuario',
            pretty_name='wfçdfdsçv',
            matricula = '000000',
            email = 'usuario@gov.br',
            orgao = 'mpog',
            telefone = '(11)1111-1111',
            cargo = 'adm',
            setor = 'ti',
            permissao = 'Administrador',
            senha = '123',
            favoritos = ['favoritos'],
            itens = ['itens']
        )
        return user_obj

    def retorna_usuario_autenticado(email=None,matricula=None):
        if ( (email is None) and (matricula is None) ):
            return None
        elif (matricula is None):
            user_obj = Utils.create_user_obj()
            usuario = user_obj.search_user_by_email(email)
            return usuario
        else:
            user_obj = Utils.create_user_obj()
            usuario = user_obj.search_user(matricula)
            return usuario

    def create_orgao_obj():
        orgao_obj = Orgao(
            nome='Orgao',
            pretty_name='wfçdfdsçv',
            cargo='Cargo',
            coleta=60,
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117',
            url='http://api.brlight.net/api',
            api_key='123',
            gestor='gestor'
        )
        return orgao_obj

    def return_all_bases_list():
        # RETORNA TODAS AS BASES
        bases = requests.get(config.REST_URL)
        bases_dict = bases.json()
        base_list = []
        for value in bases_dict["results"]:
            base_list.append(value["metadata"]["name"])
        return base_list

    def return_base_by_name(base_name):
        # RETORNA BASE ESPECÍFICA
        base_doc = requests.get(config.REST_URL+'/'+base_name+'/doc')
        base_dict = base_doc.json()
        return base_dict

    def is_base_coleta(base_obj):
        try:
            search_in_doc = base_obj["results"][0]["win32_bios"]
            return True
        except:
            return False

    def descriptions(self, item):
        """
        Adiciona descrição para os campos.
        """
        desc = Desc()
        search = desc.search_desc(item)
        saida = dict()
        for elm in search.keys():
            saida[elm] = search[elm]

        return saida

    def create_report(self, nm_base):
        """
        Inseri Relatorio completo na base de relatorios
        """
        base_reports = ReportsBase(nm_base)
        reports_conf = ConfReports(nm_base)
        coleta_base = ColetaManualBase(nm_base)
        report = Reports(nm_base)
        itens = {
            "win32_processor": "win32_processor_manufacturer",
            "win32_bios": "win32_bios_manufacturer",
            "operatingsystem": "operatingsystem_caption",
            "win32_logicaldisk": "win32_logicaldisk_caption",
            "win32_physicalmemory": "win32_physicalmemory_memorytype",
            "softwarelist": None
        }
        #try:
        for elm in itens.keys():
            attr = elm
            child = itens[elm]
            data = report.count_attribute(attr, child)
            for element in data:
                data_json = {
                    attr: {
                        attr+'_item': str(element),
                        attr+'_amount': str(data[element])
                    }
                }
                document = json.dumps(data_json)
                reports_conf.create_coleta(document)
        return 1
        #except:
            #return 0

    @staticmethod
    def create_atividade_obj():
        atividade_obj = Atividade(
            tipo='atividade',
            usuario='José',
            descricao='breve descrição',
            data='22/03/2014'
        )
        return atividade_obj

    def check_has_user():
        user_obj = Utils.create_user_obj()
        search = user_obj.search_list_users()
        result_count = search.result_count
        return result_count > 0

    def check_has_orgao():
        orgao_obj = Utils.create_orgao_obj()
        search = orgao_obj.search_list_orgaos()
        result_count = search.result_count
        return result_count > 0
