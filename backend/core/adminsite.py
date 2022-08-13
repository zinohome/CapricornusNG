from core.settings import settings
from fastapi_user_auth.site import AuthAdminSite

from util.log import log as log

site = AuthAdminSite(settings)
auth = site.auth
site.UserAuthApp.page_schema.sort = -99