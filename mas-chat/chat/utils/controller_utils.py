import importlib
import os
from glob import glob
from typing import Callable

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chat.utils.logging_utils import initialize_logger


def create_app(project_path: str) -> FastAPI:
    """
    Creates a FastAPI application, initializes it with the local configuration,
    and includes all routers found in the project directory.

    Args:
        project_path (str): Root path of the project to create the app

    Returns:
        FastAPI: A new FastAPI application.
    """
    app = FastAPI()
    initialize_logger(project_path)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler(
        "startup",
        create_start_app_handler(),
    )
    app.add_event_handler(
        "shutdown",
        create_stop_app_handler(),
    )

    modules = get_controllers(project_path)

    for module in modules:
        router = module.router
        app.include_router(router)

    return app


def get_controllers(project_path: str):
    """
    Finds all modules with a "_controller.py" file in the given project directory.

    Args:
        project_path (str): The root directory of the project.
    """
    module_names = get_module_names(project_path, "controller")

    return [importlib.import_module(module_name) for module_name in module_names]


def get_module_names(project_path: str, pattern: str) -> list[str]:
    """
    Recursively searches the given project directory for subdirectories containing a specific pattern.

    Args:
        project_path (str): The root directory of the project.
        pattern (str): The subdirectory name pattern to search for (e.g. "controller").

    Returns:
        list[str]: A list of module names as strings.
    """
    module_names = []
    for root, dirs, files in os.walk(project_path):
        for directory in dirs:
            controller_dir = os.path.join(root, directory, pattern)
            if os.path.isdir(controller_dir):
                for controller_file in glob(
                    os.path.join(controller_dir, f"*_{pattern}.py")
                ):
                    relative_path = os.path.relpath(controller_file, start=project_path)
                    relative_path = relative_path.replace("/", ".").replace("\\", ".")
                    module_name = relative_path.rstrip(".py")
                    module_names.append(module_name)

    return module_names


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        pass

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        pass

    return stop_app
