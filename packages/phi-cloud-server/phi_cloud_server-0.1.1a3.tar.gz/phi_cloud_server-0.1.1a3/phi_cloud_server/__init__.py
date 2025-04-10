from phi_cloud_server.config import config
from phi_cloud_server.main import app
from phi_cloud_server.utils import default_dir, dev_mode

# ---------------------- 启动 ----------------------

RELOAD_DIR = "./phi_cloud_server"


def main():
    import uvicorn

    # dev启用热重载
    if dev_mode:
        import jurigged

        jurigged.watch(
            pattern=RELOAD_DIR,
        )

    uvicorn.run(app, host=config.server.host, port=config.server.port)
