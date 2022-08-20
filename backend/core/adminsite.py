#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  #
#  Copyright (C) 2021 ZinoHome, Inc. All Rights Reserved
#  #
#  @Time    : 2021
#  @Author  : Zhang Jun
#  @Email   : ibmzhangjun@139.com
#  @Software: Capricornus

from fastapi_amis_admin.admin import DocsAdmin, ReDocsAdmin

from core.settings import settings
from fastapi_user_auth.site import AuthAdminSite

from util.log import log as log

site = AuthAdminSite(settings)
auth = site.auth
site.UserAuthApp.page_schema.sort = -99
site.unregister_admin(DocsAdmin, ReDocsAdmin)

