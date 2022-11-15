#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus
import os

from fastapi import FastAPI
from utils.amis_admin.admin import DocsAdmin, ReDocsAdmin, HomeAdmin
from utils.amis_admin.amis import AmisAPI, SizeEnum
from utils.amis_admin.amis.components import App, Flex, ActionType, Drawer, Service
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.requests import Request
from core.settings import settings, Settings
from utils.user_auth.site import AuthAdminSite
from core import i18n as _
from utils.log import log as log

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(CORE_DIR, 'templates/app.html')

class CapricornusAdminSite(AuthAdminSite):
    template_name = TEMP_DIR

    def __init__(self, settings: Settings, fastapi: FastAPI = None, engine: AsyncEngine = None):
        super().__init__(settings, fastapi, engine)
        # 取消注册默认管理类
        #self.unregister_admin(HomeAdmin,DocsAdmin, ReDocsAdmin)
        self.unregister_admin(HomeAdmin, ReDocsAdmin)

    async def get_page(self, request: Request) -> App:
        app = await super().get_page(request)
        app.brandName = settings.site_title
        app.logo = '/static/images/logo.png'
        user_auth_app = self.get_admin_or_create(self.UserAuthApp)
        for item in app.header.items:
            if item.type == 'dropdown-button' and item.label == f"{request.user.username}":
                app.header.items.remove(item)
        app.header = Flex(className="w-full", justify='flex-end', alignItems='flex-end', items=[app.header, {
            "type": "dropdown-button",
            "label": f"{request.user.username}",
            "trigger": "hover",
            "icon": "fa fa-user",
            "buttons": [
                ActionType.Drawer(
                    label=_('User Profile'),
                    drawer=Drawer(
                        title=_('User Profile'),
                        position="right",
                        showCloseButton=True,
                        overlay=False,
                        closeOnOutside=False,
                        actions=[],
                        size=SizeEnum.md,
                        body=Service(
                            schemaApi=AmisAPI(
                                method='post',
                                url=f"{user_auth_app.router_path}/form/userinfo",
                                cache=600000,
                                responseData={'&': '${body}'}
                            )))),
                ActionType.Url(
                    label=_('Sign out'),
                    url=f"{user_auth_app.router_path}/logout",
                    blank=False
        ),
            ]
        }])
        return app


site = CapricornusAdminSite(settings)
auth = site.auth
site.UserAuthApp.page_schema.sort = -99

