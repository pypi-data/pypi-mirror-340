import sys
import os
import signal
import dotenv
from typing import Optional, Any


dotenv.load_dotenv()
sys.dont_write_bytecode = True

import uvicorn
from carpenter_py.server import create_app
from carpenter_py.utils.log import logger
from carpenter_py.settings import CarpenterConfig


def run(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = True,
    debug: bool = True,
    config: Optional[CarpenterConfig] = None,
    **kwargs: Any,
) -> None:
    """
    Run the development server

    Args:
        host: Host address to bind the server to
        port: Port number to listen on
        reload: Whether to enable auto-reload on file changes
        debug: Whether to run in debug mode
        config: Optional CarpenterConfig instance
        **kwargs: Additional keyword arguments to pass to run_server
    """
    signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))  # Ctrl+C
    signal.signal(signal.SIGTERM, lambda s, f: sys.exit(0))  # kill

    app_config = config or CarpenterConfig()
    logger.info("[CARPENTER] > Development server starting...")

    if reload:
        logger.info("[CARPENTER] > Auto-reload is enabled. Press Ctrl+C to stop.")

    os.environ["CARPENTER_ENVIRONMENT"] = "development"

    if debug:
        os.environ["CARPENTER_DEBUG"] = "true"
        logger.info("Debug mode is enabled")

    try:
        if reload:
            uvicorn.run(
                "carpenter_py.server:create_app",
                host=host,
                port=port,
                reload=True,
                reload_dirs=[
                    "carpenter",
                    "pages",
                ],
                log_level=app_config.LOG_LEVEL,
                factory=True,
            )
        else:
            app = create_app(config=app_config, debug=debug)
            uvicorn.run(
                app,
                host=host,
                port=port,
                debug=app_config.DEBUG,
                log_level=app_config.LOG_LEVEL,
            )
    except KeyboardInterrupt:
        logger.info("[CARPENTER] > Development server stopped by user")
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        logger.exception(f"[CARPENTER] > Development server failed: {str(e)}")
        sys.exit(1)


def create_dev_app(**kwargs: Any) -> Any:
    """
    Create a development application instance
    This is useful for testing and debugging

    Args:
        **kwargs: Configuration options for the application

    Returns:
        The ASGI application instance
    """
    from carpenter_py.server import create_app

    # Set development environment
    os.environ["CARPENTER_ENVIRONMENT"] = "development"
    os.environ["CARPENTER_DEBUG"] = "true"

    # Create and return the app
    app = create_app(**kwargs)
    return app
