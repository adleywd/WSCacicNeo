#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
from wscacicneo.model.orgao import Orgao
from wscacicneo.model.orgao import OrgaoBase
from liblightbase.lbbase.struct import Base
from liblightbase.lbutils import conv

class TestOrgaoBase(unittest.TestCase):
    """
    Testa base do órgão no LB
    """
    def setUp(self):
        """
        Carregando atributos genéricos do teste
        """
        self.documentrest = OrgaoBase().documentrest

    def test_orgao_attributes(self):
        """
        Insere atributos na base órgãos
        """
        orgao_obj = Orgao(
            nome='Ministério do Planejameiaaaaaaaaanto',
            cargo='cargo',
            coleta='4h',
            sigla='MPOG',
            endereco='Esplanada bloco C',
            email='admin@planemaneto.gov.br',
            telefone='(61) 2025-4117'
        )
        results = orgao_obj.create_orgao()
        var_file = open("results.txt", "w")
        cont = var_file.write(str(results))
        var_file.close()

        assert(type(results) ==  int)

    def test_delete_attributes(self):
        """
        Deleta doc apartir do id
        """
        nm_orgao = 'Ministério do Planejameiaaaaaaaaanto',
        search = Orgao().search_orgao(nm_orgao)
        id = search['_metadata']['id_doc']
        delete = Orgao().delete_orgao(id)

        assert(delete == 'DELETED')


    def tearDown(self):
        """
        Apaga dados do teste
        """
        pass
