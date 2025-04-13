import sys
import dotenv

sys.dont_write_bytecode = True
dotenv.load_dotenv()
import sys
from carpenter_py.env import project_root

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from carpenter_py.env import project_root
import os
import atexit
import subprocess
import contextlib
import threading
import signal
from typing import Optional, Any, List, Callable
from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.routing import Route
from starlette.responses import JSONResponse
from carpenter_py.actions import (
    get_action_routes,
    import_page_actions,
    get_action_metadata,
    get_action_docs,
    export_action_type_map,
)
from carpenter_py.utils.generate_ts_types import generate_typescript_types
from carpenter_py.middleware.authorization import AuthorizationMiddleware
from carpenter_py.utils.page_mapper import map_page_routes
from carpenter_py.settings import CarpenterConfig
from carpenter_py.utils.log import logger

frontend_process = None


def _stream_output(process, prefix="Frontend"):
    """Stream output from subprocess to logger with handling for Unicode characters"""
    for line in iter(process.stdout.readline, b""):
        try:
            decoded = line.decode("utf-8").strip()
            if decoded and ("error" in decoded.lower() or "fail" in decoded.lower()):
                decoded = decoded.encode("cp1252", errors="replace").decode("cp1252")
                logger.error(f"{prefix}: {decoded}")
            else:
                logger.debug(f"{prefix}: {decoded}")
        except Exception:
            pass


def start_frontend(package_manager="npm", command="dev", port=None):
    """
    Start the frontend Vite dev server using specified package manager and command

    Args:
        package_manager: Package manager to use (npm, yarn, pnpm)
        command: Command to run (dev, build, start)
        port: Optional port override for the frontend server
    """

    global frontend_process
    try:
        cwd = project_root

        cmd_ext = ".cmd" if os.name == "nt" else ""

        cmd = [f"{package_manager}{cmd_ext}", "run", command]

        frontend_process = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        output_thread = threading.Thread(
            target=_stream_output, args=(frontend_process, "Frontend"), daemon=True
        )
        output_thread.start()

        return frontend_process

    except Exception as e:
        logger.error(f"[CARPENTER] > Failed to start frontend server: {str(e)}")
        return None


def stop_frontend():
    """Gracefully shut down the frontend dev process"""
    global frontend_process
    if frontend_process and frontend_process.poll() is None:
        try:
            if os.name != "nt":
                frontend_process.send_signal(signal.SIGTERM)

            frontend_process.terminate()
            frontend_process.wait(timeout=5)
        except Exception:
            frontend_process.kill()
            frontend_process.wait()
        finally:
            logger.warning("[CARPENTER] > Shutting down Carpenter application")


@contextlib.asynccontextmanager
async def lifespan(app: Starlette):
    """
    Lifespan context manager for the Starlette application

    Args:
        app: The Starlette application instance
    """
    import_page_actions()
    routes = get_action_routes()
    for route in routes:
        app.router.routes.append(route)

    export_action_type_map()
    generate_typescript_types()

    async def dev_page_routes():
        return JSONResponse(map_page_routes())

    async def dev_action_routes():
        return JSONResponse(get_action_metadata())

    def get_dev_routes():
        return [
            Route("/__dev/actions", lambda request: JSONResponse(get_action_docs()))
        ]

    app.router.routes.append(
        Route("/_carpenter/routes", dev_page_routes, methods=["GET"])
    )
    app.router.routes.append(
        Route("/_carpenter/actions", dev_action_routes, methods=["GET"])
    )
    app.router.routes.extend(get_dev_routes())

    config = app.state.config if hasattr(app.state, "config") else None

    package_manager = (
        config.PACKAGE_MANAGER
        if config and hasattr(config, "PACKAGE_MANAGER")
        else os.environ.get("CARPENTER_PACKAGE_MANAGER", "npm")
    )
    frontend_command = (
        config.FRONTEND_COMMAND
        if config and hasattr(config, "FRONTEND_COMMAND")
        else os.environ.get("CARPENTER_FRONTEND_COMMAND", "dev")
    )
    frontend_port = (
        config.VITE_PORT if config and hasattr(config, "VITE_PORT") else None
    )

    if getattr(config, "ENVIRONMENT", "development").lower() == "development":
        start_frontend(
            package_manager=package_manager,
            command=frontend_command,
            port=frontend_port,
        )
        atexit.register(stop_frontend)

    logger.info("--------------------------------------------------")
    logger.info("[CARPENTER] > Carpenter application started")
    logger.info(f"[CARPENTER] > Environment             : {config.ENVIRONMENT.upper()}")
    logger.info(f"[CARPENTER] > Debug mode              : {'ON' if config.DEBUG else 'OFF'}")
    logger.info(f"[CARPENTER] > Log level               : {config.LOG_LEVEL}")
    logger.info(f"[CARPENTER] > Client command          : {frontend_command}")
    if frontend_port:
        logger.info(f"[CARPENTER] > Client                  : http://localhost:{frontend_port}")
    logger.info("--------------------------------------------------")

    yield


def create_app(
    config: Optional[CarpenterConfig] = None,
    debug: bool = True,
    middlewares: Optional[List[Callable]] = None,
    static_dir: str = "public",
    static_url: str = "/static",
    **kwargs: Any,
) -> Starlette:
    """
    Create and configure the Starlette application

    Args:
        config: Optional CarpenterConfig instance
        debug: Whether to run in debug mode
        middlewares: List of additional middleware to add
        static_dir: Directory for static files
        static_url: URL path for static files
        **kwargs: Additional keyword arguments passed to Starlette

    Returns:
        Configured Starlette application
    """
    app = Starlette(debug=debug, lifespan=lifespan, **kwargs)

    app.state.config = config or CarpenterConfig()

    app.add_middleware(AuthorizationMiddleware)
    if middlewares:
        for middleware in middlewares:
            app.add_middleware(middleware)

    try:
        if not os.path.exists(static_dir):
            os.makedirs(static_dir, exist_ok=True)

        app.mount(static_url, StaticFiles(directory=static_dir), name="static")
    except Exception as e:
        logger.error(f"[CARPENTER] > Failed to mount static files: {str(e)}")

    return app
