#!/usr/env python
# -*- coding: utf-8 -*-asdasd

# # 1. carregar usuário da sessão
# # 2. carregar objeto usuário
# # 3. pegar grupo do usuário

from wscacicneo.model.user import User
from wscacicneo.utils.utils import Utils


def groupfinder(userid, request):
    # Primeiro tenta busca pela chave de API
    vars_dict = request.GET
    print(vars_dict)
    api_key = vars_dict.get('api_key')
    if api_key is not None:
        return ['Orgao']
    user_obj = Utils.create_user_obj()
    usuario = user_obj.search_user_by_email(userid)
    permissao = usuario.results[0].permissao
    return [permissao]
