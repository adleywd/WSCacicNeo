#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import json
import datetime
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config, forbidden_view_config
from wscacicneo.model import orgao as model_orgao
from wscacicneo.utils.utils import Utils
from wscacicneo.model.orgao import Orgao
from ..model import atividade
from liblightbase.lbutils import conv
from .. import config
from .. import search
import uuid
import ast
from pyramid.session import check_csrf_token

class Orgaos(object):
    """
    Views de notificação
    """
    def __init__(self, request):
        """
        Método construtor
        :param request: Requisição
        """
        self.request = request
        self.usuario_autenticado = Utils.retorna_usuario_autenticado(
            self.request.session.get('userid'))

    def listorgao(self):
        orgao_obj = Utils.create_orgao_obj()
        search = orgao_obj.search_list_orgaos()
        return {'orgao_doc': search.results,
                'usuario_autenticado': self.usuario_autenticado
                }

    def get_orgao_initial(self):
        if Utils.check_has_orgao(): # se tiver orgao
            return HTTPFound(location = self.request.route_url('login'))
        return {'api_key': uuid.uuid4()}

    def post_orgao_initial(self):
        if Utils.check_has_orgao(): # se tiver orgao
            return HTTPFound(location = self.request.route_url('login'))
        return self.post_orgao()

    def config_orgao(self):
        sigla = self.request.matchdict['sigla']

        search_obj = search.orgao.SearchOrgao(
            param=sigla
        )
        orgao_obj = search_obj.search_by_name()

        saida = orgao_obj.orgao_to_dict()
        # Coloca algum valor na URL
        if saida.get('url') is None:
            saida['url'] = self.request.application_url

        saida['usuario_autenticado'] = self.usuario_autenticado

        return saida

    def editorgao(self):
        sigla = self.request.matchdict['sigla']
        search_obj = search.orgao.SearchOrgao(
            param=sigla
        )
        orgao_obj = search_obj.search_by_name()

        saida = orgao_obj.orgao_to_dict()
        if saida.get('url') is None:
            saida['url'] = self.request.application_url
        saida['usuario_autenticado'] = self.usuario_autenticado

        return saida

    def post_orgao(self):
        """
        Post doc órgãos
        """
        rest_url = config.REST_URL
        orgaobase = model_orgao.OrgaoBase().lbbase
        doc = self.request.params
        nome_base = Utils.format_name(doc.get('sigla'))
        orgao_obj = Orgao(
            nome=nome_base,
            pretty_name=doc.get('pretty_name'),
            cargo=doc.get('cargo'),
            gestor=doc.get('gestor'),
            coleta=int(doc.get('coleta')),
            sigla=doc.get('sigla'),
            endereco=doc.get('end'),
            email=doc.get('email'),
            telefone=doc.get('telefone'),
            url=doc.get('url'),
            habilitar_bot=ast.literal_eval(doc.get('habilitar_bot')),
            api_key=doc.get('api_key')
        )
        try:
            if self.usuario_autenticado is None:
                user = 'Sistema'
            else:
                user = self.usuario_autenticado.nome
        except IndexError:
            user = 'Sistema'

        at = atividade.Atividade(
            tipo='insert',
            usuario=user,
            descricao='Cadastrou o órgão ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()
        id_doc = orgao_obj.create_orgao()
        session = self.request.session
        session.flash('Orgão cadastrado com sucesso', queue="success")
        return Response(str(id_doc))

    def put_orgao(self):
        """
        Edita um doc apartir do id
        """
        doc = self.request.params
        sigla = doc['id']
        nome_base = Utils.format_name(doc.get('sigla'))
        orgao_obj = Orgao(
            nome=nome_base,
            pretty_name=doc.get('pretty_name'),
            gestor=doc.get('gestor'),
            cargo=doc.get('cargo'),
            coleta=int(doc.get('coleta')),
            sigla=nome_base,
            endereco=doc.get('end'),
            email=doc.get('email'),
            telefone=doc.get('telefone'),
            url=doc.get('url'),
            habilitar_bot=ast.literal_eval(doc.get('habilitar_bot')),
            api_key=doc.get('api_key')
        )
        at = atividade.Atividade(
            tipo='put',
            usuario=self.usuario_autenticado.nome,
            descricao='Alterou o órgão ' + nome_base,
            data=datetime.datetime.now()
        )
        at.create_atividade()
        orgao = orgao_obj.orgao_to_dict()
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        doc = json.dumps(orgao)
        edit = orgao_obj.edit_orgao(id, doc)
        session = self.request.session
        session.flash('Alteração realizado com sucesso', queue="success")
        return Response(edit)

    def delete_orgao(self):
        """
        Deleta doc apartir do id
        """
        session = self.request.session
        doc = self.request.params
        sigla = self.request.matchdict['sigla']
        orgao_obj = Utils.create_orgao_obj()
        at = atividade.Atividade(
            tipo='delete',
            usuario=self.usuario_autenticado.nome,
            descricao='Removeu o órgão '+ sigla,
            data=datetime.datetime.now()
        )
        at.create_atividade()
        search = orgao_obj.search_orgao(sigla)
        id = search.results[0]._metadata.id_doc
        delete = orgao_obj.delete_orgao(id)

        if(delete):
            session.flash('Sucesso ao apagar o órgão '+search.results[0].nome, queue="success")
        else:
            session.flash('Ocorreu um erro ao apagar o órgão '+search.results[0].nome, queue="error")
        return HTTPFound(location=self.request.route_url('listorgao'))

    # Views de Orgão
    def orgao(self):
        return {
            'usuario_autenticado': self.usuario_autenticado,
            'api_key': uuid.uuid4()
        }
