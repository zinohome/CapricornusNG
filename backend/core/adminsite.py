from core.settings import settings


from fastapi_user_auth.site import AuthAdminSite

site = AuthAdminSite(settings)
auth = site.auth



#from fastapi_scheduler import SchedulerAdmin

#scheduler = SchedulerAdmin.bind(site)

