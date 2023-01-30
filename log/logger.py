from uvicorn.workers import UvicornWorker


class EliteUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {
        "log_config": "log/logging.yaml",
    }
