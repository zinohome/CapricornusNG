from fastapi import FastAPI


def setup(app: FastAPI):
    # 1. 导入数据应用
    from . import dataadmin
    # 2. 导入管理应用
    from . import admin
    # 3. 导入定时任务
    from . import jobs
    # 4. 注册普通路由
    from . import apis
    app.include_router(apis.router)
    # 5. 注册数据路由
    from . import dataapis


