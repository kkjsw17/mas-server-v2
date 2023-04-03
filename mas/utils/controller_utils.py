import importlib
import os
from glob import glob

from fastapi import FastAPI

from mas.container import Initializer


def create_app() -> FastAPI:
    """
    Creates a FastAPI application, initializes it with the local configuration, and includes all routers found in the
    project directory.

    Returns:
        FastAPI: A new FastAPI application.
    """
    Initializer("local")

    app = FastAPI()
    modules = get_controllers("./")

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
