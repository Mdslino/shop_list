from uvicorn.workers import UvicornWorker


class FactoryUvirocnWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "uvloop", "http": "httptools", "factory": True, 'access_log': True, 'use_colors': True}
