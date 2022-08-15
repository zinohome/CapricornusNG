from fastapi import FastAPI
from util.log import log as log

def setup(app: FastAPI):
    # 1. 导入管理应用
    from . import admin
    # 2. 导入定时任务
    from . import jobs
    # 3. 注册普通路由
    from . import apis
    app.include_router(apis.router)
    # 4. 注册数据路由
    from . import dataapis
    app.include_router(dataapis.router)


