#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'macieski'

from requests.exceptions import HTTPError
from wscacicneo import config
import logging
from liblightbase.lbbase.struct import Base, BaseMetadata
from liblightbase.lbbase.lbstruct.group import *
from liblightbase.lbbase.lbstruct.field import *
from liblightbase.lbbase.content import Content
from liblightbase.lbrest.base import BaseREST
from liblightbase.lbrest.document import DocumentREST
from liblightbase.lbutils import conv
from liblightbase.lbsearch.search import Search, OrderBy

log = logging.getLogger()

class BaseBackup():
    """
    Classe para a base de usuários
    """
    def __init__(self, rest_url=None):
        """
        Método construtor
        """
        print(rest_url)
        if rest_url is None:
            self.rest_url = config.REST_URL
        else:
            self.rest_url = rest_url
        self.baserest = BaseREST(rest_url=self.rest_url, response_object=True)
        self.documentrest = DocumentREST(rest_url=self.rest_url,
                base=self.lbbase, response_object=False)

    @property
    def lbbase(self):

        """
        COnfiguração da Coleta
        """
        data_coleta = Field(**dict(
            name='data_coleta',
            description='Data da Coleta',
            alias='data_coleta',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=True
        ))

        nome_orgao = Field(**dict(
            name='nome_orgao',
            description='Nome do Órgão',
            alias='nome_orgao',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        """
        LB Processadores
        """
        Win32_Processor_Manufacturer = Field(**dict(
            name='Win32_Processor_Manufacturer',
            description='Win32_Processor_Manufacturer',
            alias='Win32_Processor_Manufacturer',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        Win32_Processor_NumberOfLogicalProcessors = Field(**dict(
            name='Win32_Processor_NumberOfLogicalProcessors',
            description='Win32_Processor_NumberOfLogicalProcessors',
            alias='Win32_Processor_NumberOfLogicalProcessors',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        
        Win32_Processor_Caption = Field(**dict(
            name='Win32_Processor_Caption',
            description='Win32_Processor_Caption',
            alias='Win32_Processor_Caption',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        """
        LB Sistema Operacional
        """
        OperatingSystem_Version = Field(**dict(
            name='OperatingSystem_Version',
            description='OperatingSystem_Version',
            alias='OperatingSystem_Version',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        OperatingSystem_InstallDate = Field(**dict(
            name='OperatingSystem_InstallDate',
            description='OperatingSystem_InstallDate',
            alias='OperatingSystem_InstallDate',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
        OperatingSystem_Caption = Field(**dict(
            name='OperatingSystem_Caption',
            description='OperatingSystem_Caption',
            alias='OperatingSystem_Caption',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))

        """
        LB SoftwareList
        """
        SoftwareList = Field(**dict(
            name='SoftwareList',
            description='SoftwareList',
            alias='SoftwareList',
            datatype='Text',
            indices=['Textual'],
            multivalued=True,
            required=False
        ))

        """
        LB Bios
        """
        Win32_BIOS_Manufacturer = Field(**dict(
            name='Win32_BIOS_Manufacturer',
            description='Win32_BIOS_Manufacturer',
            alias='Win32_BIOS_Manufacturer',
            datatype='Text',
            indices=['Textual'],
            multivalued=False,
            required=False
        ))
       
        """
        GROUP Sistema Operacional
        """
        OperatingSystem_content = Content()
        OperatingSystem_content.append(OperatingSystem_Version)
        OperatingSystem_content.append(OperatingSystem_InstallDate)
        OperatingSystem_content.append(OperatingSystem_Caption)

        OperatingSystem_metadata = GroupMetadata(
            name='OperatingSystem',
            alias='OperatingSystem',
            description='OperatingSystem',
            multivalued = False
        )

        OperatingSystem = Group(
            metadata = OperatingSystem_metadata,
            content = OperatingSystem_content
        )

        """
        GROUP Bios
        """
        Win32_BIOS_content = Content()
        Win32_BIOS_content.append(Win32_BIOS_Manufacturer)

        Win32_BIOS_metadata = GroupMetadata(
            name='Win32_BIOS',
            alias='Win32_BIOS',
            description='Win32_BIOS',
            multivalued = False
        )

        Win32_BIOS = Group(
            metadata = Win32_BIOS_metadata,
            content = Win32_BIOS_content
        )

    
        """
        GROUP Processador
        """
        Win32_Processor_content = Content()
        Win32_Processor_content.append(Win32_Processor_Manufacturer)
        Win32_Processor_content.append(Win32_Processor_NumberOfLogicalProcessors)
        Win32_Processor_content.append(Win32_Processor_Caption)

        Win32_Processor_metadata = GroupMetadata(
            name='Win32_Processor',
            alias='Win32_Processor',
            description='Win32_Processor',
            multivalued = False
        )

        Win32_Processor = Group(
            metadata = Win32_Processor_metadata,
            content = Win32_Processor_content
        )

        base_metadata = BaseMetadata(
            name = 'orgaos_bk',
        )

        content_list = Content()
        content_list.append(nome_orgao)
        content_list.append(data_coleta)
        content_list.append(Win32_Processor)
        content_list.append(OperatingSystem)
        content_list.append(Win32_BIOS)
        content_list.append(SoftwareList)

        lbbase = Base(
            metadata=base_metadata,
            content=content_list
        )

        return lbbase

    @property
    def metaclass(self):
        """
        Retorna metaclass para essa base
        """
        return self.lbbase.metaclass()

    def create_base(self):
        """
        Cria base no LB
        """
        response = self.baserest.create(self.lbbase)
        if response.status_code == 200:
            return self.lbbase
        else:
            return None

    def remove_base(self):
        """
        Remove base from Lightbase
        :param lbbase: LBBase object instance
        :return: True or Error if base was not excluded
        """
        response = self.baserest.delete(self.lbbase)
        if response.status_code == 200:
            return True
        else:
            raise IOError('Error excluding base from LB')

    def is_created(self):
        """
        Retorna se a base já existe
        """
        try:
            response = self.baserest.get(self.lbbase.metadata.name)
            return True
        except:
            return False