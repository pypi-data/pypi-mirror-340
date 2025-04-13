#!/usr/bin/env python
"""
Carpenter CLI - Command line interface for the Carpenter framework
"""
import sys
import dotenv
import argparse
from typing import Optional, List
from rich.console import Console
from carpenter_py.settings import CarpenterConfig
from carpenter_py.utils.log import logger
from scripts import build, dev
import os
from carpenter_py.env import project_root

sys.dont_write_bytecode = True

# Ensure the current working directory is the project root
os.chdir(project_root)

# Load environment variables from .env at the project root
dotenv.load_dotenv(os.path.join(project_root, ".env"))

console = Console()


class Context:
    """A container to hold shared context like config, args, etc."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.config = CarpenterConfig(
            env_file=os.path.join(project_root, args.env_file)
        )
        self.logger = logger


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Carpenter - A web application framework",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Dev command
    dev_parser = subparsers.add_parser("dev", help="Run the development server")
    dev_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="Port number for the server"
    )
    dev_parser.add_argument(
        "--host", default="127.0.0.1", help="Host address to bind the server"
    )
    dev_parser.add_argument(
        "--env-file", default=".env", help="Path to environment file"
    )
    dev_parser.add_argument(
        "--log-level",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level",
    )

    # Build command
    build_parser = subparsers.add_parser(
        "build", help="Build the application for production"
    )
    build_parser.add_argument(
        "--no-minify", action="store_true", help="Skip minification during build"
    )

    # Migrate command
    subparsers.add_parser("migrate", help="Run database migrations")

    # Shell command
    subparsers.add_parser(
        "shell", help="Start an interactive shell with the application context"
    )

    return parser.parse_args(args)


def collect_commands():
    """Dynamically collect command functions"""
    return {
        name.replace("run_", ""): func
        for name, func in globals().items()
        if name.startswith("run_") and callable(func)
    }


def run_dev(ctx: Context) -> None:
    """Run the development server"""
    console.print("[bold green]Starting development server...[/]")
    dev.run(
        host=ctx.args.host,
        port=ctx.args.port,
        debug=ctx.config.DEBUG,
        log_level=ctx.args.log_level,
        reload=True,
        reload_dirs=["carpenter", "app", "pages"],
        factory=True,
    )


def run_build(ctx: Context) -> None:
    """Build the application for production"""
    console.print("[bold green]Building application for production...[/]")
    build.build(prod=True, minify=not ctx.args.no_minify)
    console.print("[bold green]Build completed successfully![/]")


def run_migrate(ctx: Context) -> None:
    """Run database migrations"""
    console.print("[bold yellow]Running database migrations...[/]")
    try:
        from carpenter import migrations

        migrations.run_migrations()
        console.print("[bold green]Migrations completed successfully![/]")
    except Exception:
        console.print_exception()
        sys.exit(1)


def run_shell(ctx: Context) -> None:
    """Start an interactive shell with the application context"""
    console.print("[bold blue]Starting interactive shell...[/]")
    import code

    variables = {"config": ctx.config, "logger": ctx.logger}
    code.interact(local=variables, banner="Carpenter Interactive Shell")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the Carpenter CLI"""
    parsed_args = parse_args(args)

    # Set up logging
    logger.setLevel(parsed_args.log_level.upper())

    # Initialize context
    ctx = Context(parsed_args)

    # Command dispatcher
    commands = collect_commands()

    # Run the requested command
    try:
        if parsed_args.command in commands:
            commands[parsed_args.command](ctx)
            return 0
        else:
            console.print(f"[bold red]Unknown command: {parsed_args.command}[/]")
            return 1
    except Exception:
        console.print_exception()
        return 1


def app():
    """Main entry point for the Carpenter CLI"""
    return main()
