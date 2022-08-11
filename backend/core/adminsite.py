from core.settings import settings
from fastapi_user_auth.site import AuthAdminSite

site = AuthAdminSite(settings)
auth = site.auth