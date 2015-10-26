#!/usr/env python
# -*- coding: utf-8 -*-

import json
import re
import logging
from pyramid.view import view_config
from pyramid.response import Response
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils
from wscacicneo.model import base_reports
from wscacicneo.model import config_reports
from wscacicneo.model import reports
from wscacicneo.model import all_reports
from wscacicneo.model import descriptions
from wscacicneo.model.reports import Reports
from wscacicneo.search.orgao import SearchOrgao
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import NullDocument
from random import randint
from pyramid.session import check_csrf_token
from pyramid.httpexceptions import HTTPFound
import requests
import psycopg2
from wscacicneo import config

log = logging.getLogger()


class Relacional(object):
    """
    Métodos básicos do sistema
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))
        self.host = "localhost"
        self.database = "lb_relacional"
        self.user_db = "rest"
        self.password_db = "rest"

    #@view_config(route_name='conf_csv', renderer='../templates/conf_csv.pt')

    def conf_csv(self):
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()

        return {'orgao_doc': result,
                'usuario_autenticado': self.usuario_autenticado
                }

    def lbrelacional_csv(self):
        try:
            listaorgaos = self.request.params.getall('orgao')
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
            cur = conn.cursor()
            if len(listaorgaos) == 1:
                cur.execute("SELECT * FROM cacic_relacional.cacic_relacional WHERE name_orgao = '{0}'".format(listaorgaos[0]))
            else:
                cur.execute("SELECT * FROM cacic_relacional.cacic_relacional WHERE name_orgao in {0}".format(tuple(listaorgaos)))
            rows = cur.fetchall()
            cur.execute("SELECT * FROM cacic_relacional.cacic_relacional LIMIT 0")
            header = [desc[0] for desc in cur.description]
            filename = 'tabela_relacional' + '.csv'
            self.request.response.content_disposition = 'attachment;filename=' + filename
            conn.close()
            return {
                'header': header,
                'rows': rows
            }
        except Exception as error:
            session = self.request.session
            print(error)
            session.flash('É necessário gerar o banco de dados relacional antes de exportá-lo!', queue="error")
            return HTTPFound(location=self.request.route_url("conf_csv"))

    def generate_relacional(self):
        list_orgaos = []
        search_obj = SearchOrgao()
        result = search_obj.list_by_name()
        for item in result:
            list_orgaos.append(item.nome)
        headers = {'Content-Type': 'application/json'}
        database_name = "cacic_relacional"
        # Verifica se o Schema já existe
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
        cur = conn.cursor()
        try:
            cur.execute("DROP SCHEMA "+database_name+" CASCADE;")
            conn.commit()
            conn.close()
        except Exception as error:
            log.error("Drop database error:", error)

        for orgao_name in list_orgaos:
            # Pega  url da base e do orgão
            orgao_base_results = requests.get(config.REST_URL+"/"+orgao_name)
            # Pega e cria json e cria tabela no banco relacional
            orgao_table = json.loads(orgao_base_results.text)
            orgao_table_model = orgao_table["metadata"]["model"]
            orgao_table_model["name_orgao"] = "Text"
            try:
                verify_hash = orgao_table["metadata"]["model"]["hash_machine"]
            except:
                orgao_table_model["hash_machine"] = "Text"

            json_data = json.dumps(orgao_table_model)
            relacional_path = "http://127.0.1.1:5000"+"/sqlapi/lightbase/tables/"+database_name
            postRelacional = requests.post(relacional_path, data=json_data, headers=headers)

            # Verifica registro por registro e adiciona o campo name_orgao
            orgao_doc_results = requests.get(config.REST_URL+"/"+orgao_name+"/doc")
            orgao_doc = json.loads(orgao_doc_results.text)
            orgao_doc = orgao_doc["results"]
            # Verifica se os databases já foram criados.
            select = self.try_select(database_name)
            while not select:
                select = self.try_select(database_name)

            for item in orgao_doc:
                item["name_orgao"] = orgao_name
                item.pop("_metadata", None)
                if not item["softwarelist"]:
                    print("entrei")
                    item.pop("softwarelist", None)
                json_data_doc = json.dumps(item)
                relacional_path = "http://127.0.1.1:5000"+"/sqlapi/lightbase/content/"+database_name
                postRelacionalDoc = requests.post(relacional_path, data=json_data_doc, headers=headers)
        session = self.request.session
        session.flash('O banco de dados relacional foi gerado com sucesso', queue="success")
        return HTTPFound(location=self.request.route_url("conf_csv"))

    def try_select(self, database_name):
        try:
            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user_db, password=self.password_db)
            cur = conn.cursor()
            cur.execute("SELECT * FROM "+database_name+"."+database_name)
            return True
        except Exception as error:
            return False
