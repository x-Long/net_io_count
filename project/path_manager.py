import os


class PathManager:
    project_dir = os.path.abspath(os.path.dirname(__file__))
    icon_dir = os.path.join(project_dir, "asset")
