from pydantic import BaseSettings, Field, validator, root_validator

class Settings(BaseSettings):
    """项目配置"""
    host: str = '127.0.0.1'
    port: int = 8000
    debug: bool = False
    version: str = '0.0.0'
    site_title: str = 'FastAPI Amis Admin'
    site_icon: str = 'https://baidu.gitee.io/amis/static/favicon_b3b0647.png'
    site_url: str = ''
    root_path: str = '/admin'
    database_url_async: str = Field('', env = 'DATABASE_URL_ASYNC')
    database_url: str = Field('', env = 'DATABASE_URL')
    language: str = ''  # 'zh_CN','en_US'
    amis_cdn: str = 'https://unpkg.com'
    amis_pkg: str = 'amis@1.10.2'
    app_exception_detail: bool = Field('', env='APP_EXCEPTIONN_DETAIL')
    app_mode: str = Field('', env='APP_MODE')
    app_profile: str = Field('', env='APP_PROFILE')
    app_log_level: str = Field('', env='APP_LOG_LEVEL')
    app_log_filename: str = Field('', env='APP_LOG_FILENAME')

    @validator('amis_cdn', 'root_path', 'site_url', pre = True)
    def valid_url(url: str):
        return url[:-1] if url.endswith('/') else url

    @root_validator(pre = True)
    def valid_database_url(cls, values):
        if not values.get('database_url') and not values.get('database_url_async'):
            values.setdefault('database_url', 'sqlite+aiosqlite:///amisadmin.db?check_same_thread=False')
        return values
