import importlib
import os
from glob import glob


def get_controllers(project_path: str):
    """

    Args:
        project_path (str): path of this project
    """
    module_names = []

    for root, dirs, files in os.walk(project_path):
        for directory in dirs:
            controller_dir = os.path.join(root, directory, "controller")
            if os.path.isdir(controller_dir):
                for controller_file in glob(
                    os.path.join(controller_dir, "*_controller.py")
                ):
                    relative_path = os.path.relpath(controller_file, start=project_path)
                    relative_path = relative_path.replace("/", ".").replace("\\", ".")
                    module_name = relative_path.rstrip(".py")
                    module_names.append(module_name)

    return [importlib.import_module(module_name) for module_name in module_names]
